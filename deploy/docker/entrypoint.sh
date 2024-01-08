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
  # chown -R kea:kea /etc/kea
  # chown -R kea:kea /var/lib/kea
  # chown -R kea:kea /var/log/kea
  # chown -R kea:kea /var/run/kea
  
  # Set up Supervisor
  mkdir -p /var/log/supervisor/
  # chown -R root:root /var/log/supervisor/
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

echo "Initializing application environment..."

# Initialize the application environment
initialize_app

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
supervisord -j /run/supervisord.pid -c /etc/supervisor/supervisord.conf
