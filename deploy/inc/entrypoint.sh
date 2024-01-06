#!/usr/bin/env bash

DB_CONNECT_RETRIES=20
DB_BACKEND=mysql
DB_USER=root
DB_PASSWORD="${KEA_DB_ROOT_PASSWORD}"

configure_kea_admin () {
  if [ "$KEA_DB_TYPE" == "postgresql" ]; then
    DB_BACKEND=pgsql
    DB_USER="${KEA_DB_USER}"
    DB_PASSWORD="${KEA_DB_PASSWORD}"
  fi
}

initialize_app () {
  # Set up Kea
  mkdir -p /etc/kea
  mkdir -p /var/lib/kea
  mkdir -p /var/log/kea
  mkdir -p /var/run/kea
  chown -R root:root /etc/kea
  chown -R root:root /var/lib/kea
  chown -R root:root /var/log/kea
  chown -R root:root /var/run/kea
  
  # Set up Supervisor
  mkdir -p /var/log/supervisor/
  chown -R root:root /var/log/supervisor/
}

initialize_db () {
  # Updates some of the input parameters of the kea-admin tool based on environment
  configure_kea_admin

  # Run the database initialization process provided by the kea-admin tool
  kea-admin db-init "${DB_BACKEND}" -h "${KEA_DB_HOST}" -P "${KEA_DB_PORT}" -u "${DB_USER}" -p "${DB_PASSWORD}" -n "${KEA_DB_NAME}"
}

upgrade_db () {
  # Updates some of the input parameters of the kea-admin tool based on environment
  configure_kea_admin

  # run the databaser upgrade process provided by the kea-admin tool
  kea-admin db-upgrade "${DB_BACKEND}" -h "${KEA_DB_HOST}" -P "${KEA_DB_PORT}" -u "${DB_USER}" -p "${DB_PASSWORD}" -n "${KEA_DB_NAME}"
}

build_config () {
  tpl_file=$(echo "$1" | xargs)
  target_path="$(echo "${2:-/etc/kea}" | xargs)"
  target_file=$(echo "$3" | xargs)
  full_tpl_path="$KHA_SHARE_PATH/tpl/$tpl_file"
  full_target_path="$target_path/$target_file"

  # Validate that the template file was given a name
  if [ "$tpl_file" == "" ]; then
    echo "No template file name provided to build_config"
    exit 1
  fi

  # Validate that the template file exists and is readable
  if [ ! -r "$full_tpl_path" ]; then
    echo "Template file $full_tpl_path does not exist or is not readable"
    exit 1
  fi

  # Validate that a target file name was provided
  if [ "$target_file" == "" ]; then
    echo "No target file name provided to build_config"
    exit 1
  fi

  # Validate that the target file is writable if it exists
  if [ -f "$full_target_path" ] && [ ! -w "$full_target_path" ]; then
    echo "Target file $full_target_path exists but is not writable"
    exit 1
  fi

  # Create the target path if it doesn't exist
  mkdir -p "$target_path"

  # Remove the existing file if it exists
  if [ -f "$full_target_path" ]; then
    rm -fr "$full_target_path"
  fi

  # Build the configuration file from the template if it exists
  if [ -f "$full_tpl_path" ]; then
    envsubst < "$full_tpl_path" > "$full_target_path"
  fi
}

# Build the service configuration files from the templates
build_configs () {
  if [[ "$KEA_HA_ENABLED" == "yes" ]]; then
    build_config "kea-dhcp4-ha.conf" "/etc/kea" "kea-dhcp4.conf"
  else
    build_config "kea-dhcp4.conf" "/etc/kea" "kea-dhcp4.conf"
  fi

  build_config "kea-ctrl-agent.conf" "/etc/kea" "kea-ctrl-agent.conf"
  build_config "supervisor-kea-agent.conf" "/etc/supervisor/conf.d" "kea-agent.conf"
  build_config "supervisor-kea-dhcp4.conf" "/etc/supervisor/conf.d" "kea-dhcp4.conf"
  build_config "supervisord.conf" "/etc/supervisor" "supervisord.conf"
}

echo "Initializing application environment..."

# Initialize the application environment
initialize_app

echo "Building service configuration files..."

# Build the service configuration files from the templates
build_configs

# If using the MySQL engine, then check if the kea database exists. If not, create it.
if [ "$KEA_DB_TYPE" == "mysql" ]; then

  echo "Initializing MySQL database..."

  # Wait for the MySQL server to become available
  until mysqladmin ping -h "${KEA_DB_HOST}" -P "${KEA_DB_PORT}" -u root -p"${KEA_DB_ROOT_PASSWORD}" --silent || [ $DB_CONNECT_RETRIES -eq 0 ]; do
    echo "Waiting for MySQL database server to become available, $((DB_CONNECT_RETRIES)) remaining attempts..."
    DB_CONNECT_RETRIES=$((DB_CONNECT_RETRIES-=1))
    sleep 1
  done

  echo "Checking if database already initialized..."

  # Check if the "lease4" tables exists in the Kea database as a rudimentary check to see if the database is ready
  table_sql="SHOW TABLES FROM ${KEA_DB_NAME}"
  tables_exist=$(mysql -h "${KEA_DB_HOST}" -P "${KEA_DB_PORT}" -u root -p"${KEA_DB_ROOT_PASSWORD}" -e "$table_sql" | grep "lease4" > /dev/null; echo "$?")

  # If the kea database is not seemingly ready, run the database initialization and upgrade processes
  if [ "$tables_exist" != "0" ]; then
    initialize_db
  fi

  echo "Upgrading database if needed..."

  # Upgrade the database if needed
  upgrade_db
fi

# If using the Postgres engine, create the kea user and database with appropriate privileges
if [ "$KEA_DB_TYPE" == "postgresql" ]; then

  echo "Initializing Postgres database..."

  export PGPASSWORD="${KEA_DB_PASSWORD}"

  test_string="${KEA_DB_HOST}:${KEA_DB_PORT} - accepting connections"

  # Wait for the Postgres server to become available
  until [ "$(pg_isready -h "${KEA_DB_HOST}" -p "${KEA_DB_PORT}" -U "${KEA_DB_USER}" -d "${KEA_DB_NAME}")" == "$test_string" ] || [ $DB_CONNECT_RETRIES -eq 0 ]; do
    echo "Waiting for Postgres database server to become available, $((DB_CONNECT_RETRIES)) remaining attempts..."
    DB_CONNECT_RETRIES=$((DB_CONNECT_RETRIES-=1))
    sleep 1
  done

  # Check if the "lease4" tables exists in the Kea database as a rudimentary check to see if the database is ready
  table_sql="SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = '${KEA_DB_SCHEMA}' AND table_name = 'lease4');"
  table_exists=$(psql -h "${KEA_DB_HOST}" -p "${KEA_DB_PORT}" -U "${KEA_DB_USER}" -d "${KEA_DB_NAME}" -c "$table_sql" | grep "f" > /dev/null; echo "$?")

  # If the kea database is not seemingly ready, run the database initialization and upgrade processes
  if [ "$table_exists" == "0" ]; then
    initialize_db
  fi

  # Upgrade the database if needed
  upgrade_db
fi

# Start the main supervisord process that spawns Kea services
supervisord -c /etc/supervisor/supervisord.conf
