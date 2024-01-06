#!/usr/bin/env bash

valid_actions="configure prepare build push install uninstall reinstall purge update start stop restart status version exit"

input_action () {
  if [ "$action" == "" ]; then
    echo -e 'What action would you like to perform?\n'
    echo -e '- Configure'
    echo -e '- Prepare'
    echo -e '- Build'
    echo -e '- Push'
    echo -e '- Install'
    echo -e '- Uninstall'
    echo -e '- Reinstall'
    echo -e '- Purge'
    echo -e '- Update'
    echo -e '- Start'
    echo -e '- Stop'
    echo -e '- Restart'
    echo -e '- Status'
    echo -e '- Version'
    echo -e '- Exit\n\n'
    read -rp "Action: " action
    # Convert the action value to lowercase
    action=$(echo "$action" | tr '[:upper:]' '[:lower:]')
  fi
}

input_confirm_action () {
  confirm_response="y"
  deny_response="n"
  action=$(echo "${1:-}" | tr '[:upper:]' '[:lower:]' | xargs)
  action_default=$(echo "${2:-$deny_response}" | tr '[:upper:]' '[:lower:]' | xargs)

  # Validate the action is one of $valid_actions
  if ! [[ "$valid_actions" =~ (^|[[:space:]])"$action"($|[[:space:]]) ]]; then
    echo "Invalid action provided. Please choose one of the following: $valid_actions"
    exit 1
  fi

  echo -e "Are you sure you want to $action the services? [$confirm_response/$deny_response]\n"
  echo -e "Default: $action_default\n"
  read -rp "Continue: " INPUT_CONFIRM
  if [ "$INPUT_CONFIRM" != "$confirm_response" ]; then
    echo "Did not receive proper confirmation of '$confirm_response' to $action services"
    exit 0
  fi
}

input_kea_image_repo_url () {
  echo -e "What is the URL for the Kea image repository? [Default: $KEA_IMAGE_REPO_URL]\n"
  read -rp "URL: " KEA_IMAGE_REPO_URL_TMP

  if [ "$KEA_IMAGE_REPO_URL_TMP" != "" ]; then
    export KEA_IMAGE_REPO_URL="$KEA_IMAGE_REPO_URL_TMP"
  fi
}

input_kea_image_repo_username () {
  echo -e "What is the username for the Kea image repository? [Default: $KEA_IMAGE_REPO_USERNAME]\n"
  read -rp "Username: " KEA_IMAGE_REPO_USERNAME_TMP

  if [ "$KEA_IMAGE_REPO_USERNAME_TMP" != "" ]; then
    export KEA_IMAGE_REPO_USERNAME="$KEA_IMAGE_REPO_USERNAME_TMP"
  fi
}

input_kea_image_repo_password () {
  echo -e "What is the password for the Kea image repository? [Default: $KEA_IMAGE_REPO_PASSWORD]\n"
  read -rp "Password: " KEA_IMAGE_REPO_PASSWORD_TMP

  if [ "$KEA_IMAGE_REPO_PASSWORD_TMP" != "" ]; then
    export KEA_IMAGE_REPO_PASSWORD="$KEA_IMAGE_REPO_PASSWORD_TMP"
  fi
}

input_kea_image_name () {
  echo -e "What is the image name for Kea? [Default: $KEA_IMAGE_REPO_NAME]\n"
  read -rp "Repository: " KEA_IMAGE_REPO_NAME_TMP

  if [ "$KEA_IMAGE_REPO_NAME_TMP" != "" ]; then
    export KEA_IMAGE_REPO_NAME="$KEA_IMAGE_REPO_NAME_TMP"
  fi
}

input_kea_version () {
  echo -e "What version of Kea would you like to use? [Default: $KEA_VERSION]\n"
  read -rp "Version: " KEA_VERSION_TMP

  if [ "$KEA_VERSION_TMP" != "" ]; then
    export KEA_VERSION="$KEA_VERSION_TMP"
  fi
}

input_kea_log_severity () {
  echo -e "What log severity would you like Kea send to STDOUT? [Default: $KEA_LOG_SEVERITY] [Options: DEBUG INFO WARN ERROR FATAL]\n"
  read -rp "Severity: " KEA_LOG_SEVERITY_TMP
  KEA_LOG_SEVERITY_TMP=$(echo "$KEA_LOG_SEVERITY_TMP" | tr '[:lower:]' '[:upper:]')

  if [ "$KEA_LOG_SEVERITY_TMP" != "" ]; then
    if ! [[ "$KEA_LOG_SEVERITY_TMP" =~ ^(DEBUG|INFO|WARN|ERROR|FATAL)$ ]]; then
      echo "Invalid response provided for log severity. Please choose DEBUG, INFO, WARN, ERROR, or FATAL."
      exit 1
    fi
    export KEA_LOG_SEVERITY="$KEA_LOG_SEVERITY_TMP"
  fi
}

input_kea_admin_user () {
  echo -e "What username would you like to use for the Kea admin user? [Default: $KEA_ADMIN_USER]\n"
  read -rp "Username: " KEA_ADMIN_USER_TMP

  if [ "$KEA_ADMIN_USER_TMP" != "" ]; then
    export KEA_ADMIN_USER="$KEA_ADMIN_USER_TMP"
  fi
}

input_kea_admin_password () {
  echo -e "What password would you like to use for the Kea admin user? [Default: $KEA_ADMIN_PASSWORD]\n"
  read -rp "Password: " KEA_ADMIN_PASSWORD_TMP

  if [ "$KEA_ADMIN_PASSWORD_TMP" != "" ]; then
    export KEA_ADMIN_PASSWORD="$KEA_ADMIN_PASSWORD_TMP"
  fi
}

input_db_type () {
  echo -e "What database engine would you like to use? [Default: $KEA_DB_TYPE] [Options: mysql postgresql]\n"
  read -rp "Database: " KEA_DB_TYPE_TMP
  KEA_DB_TYPE_TMP=$(echo "$KEA_DB_TYPE_TMP" | tr '[:upper:]' '[:lower:]')

  if [ "$KEA_DB_TYPE_TMP" != "" ]; then
    export KEA_DB_TYPE="$KEA_DB_TYPE_TMP"
  fi
}

input_db_version () {
  if [ "$KEA_DB_TYPE" == "mysql" ]; then
    export KEA_DB_VERSION="$KEA_DB_VERSION_MYSQL"
  elif [ "$KEA_DB_TYPE" == "postgresql" ]; then
    export KEA_DB_VERSION="$KEA_DB_VERSION_PGSQL"
  fi
  echo -e "What database version would you like to use? [Default: $KEA_DB_VERSION]\n"
  read -rp "Version: " KEA_DB_VERSION_TMP

  if [ "$KEA_DB_VERSION_TMP" != "" ]; then
    export KEA_DB_VERSION="$KEA_DB_VERSION_TMP"
  fi
}

input_db_host () {
  echo -e "What database host would you like to use? [Default: $KEA_DB_HOST]\n"
  read -rp "Host: " KEA_DB_HOST_TMP

  if [ "$KEA_DB_HOST_TMP" != "" ]; then
    export KEA_DB_HOST="$KEA_DB_HOST_TMP"
  fi
}

input_db_port () {
  if [ "$KEA_DB_TYPE" == "mysql" ]; then
    export KEA_DB_PORT="$KEA_DB_PORT_MYSQL"
  elif [ "$KEA_DB_TYPE" == "postgresql" ]; then
    export KEA_DB_PORT="$KEA_DB_PORT_PGSQL"
  fi
  echo -e "What database port would you like to use? [Default: $KEA_DB_PORT]\n"
  read -rp "Port: " KEA_DB_PORT_TMP

  if [ "$KEA_DB_PORT_TMP" != "" ]; then
    export KEA_DB_PORT="$KEA_DB_PORT_TMP"
  fi
}

input_db_user () {
  echo -e "What database user would you like to use? [Default: $KEA_DB_USER]\n"
  read -rp "User: " KEA_DB_USER_TMP

  if [ "$KEA_DB_USER_TMP" != "" ]; then
    KEA_DB_USER="$KEA_DB_USER_TMP"
  fi
}

input_db_password () {
  echo -e "What database password would you like to use? [Default: $KEA_DB_PASSWORD]\n"
  read -rp "Password: " KEA_DB_PASSWORD_TMP

  if [ "$KEA_DB_PASSWORD_TMP" != "" ]; then
    KEA_DB_PASSWORD="$KEA_DB_PASSWORD_TMP"
  fi
}

input_db_root_password () {
  echo -e "What database password would you like to use for the root user? [Default: $KEA_DB_ROOT_PASSWORD]\n"
  read -rp "Password: " KEA_DB_ROOT_PASSWORD_TMP

  if [ "$KEA_DB_ROOT_PASSWORD_TMP" != "" ]; then
    KEA_DB_ROOT_PASSWORD="$KEA_DB_ROOT_PASSWORD_TMP"
  fi
}

input_db_name () {
  echo -e "What database name would you like to use? [Default: $KEA_DB_NAME]\n"
  read -rp "Name: " KEA_DB_NAME_TMP

  if [ "$KEA_DB_NAME_TMP" != "" ]; then
    KEA_DB_NAME="$KEA_DB_NAME_TMP"
  fi
}

input_db_schema () {
  if [ "$KEA_DB_TYPE" == "postgresql" ]; then
    echo -e "What database schema would you like to use? [Default: $KEA_DB_SCHEMA]\n"
    read -rp "Schema: " KEA_DB_SCHEMA_TMP

    if [ "$KEA_DB_SCHEMA_TMP" != "" ]; then
      KEA_DB_SCHEMA="$KEA_DB_SCHEMA_TMP"
    fi
  fi
}

input_dhcp_interface () {
  echo -e "What network interface should be used to serve DHCP? [Default: $KEA_DHCP_INTERFACE]\n"
  read -rp "Interface: " KEA_DHCP_INTERFACE_TMP

  if [ "$KEA_DHCP_INTERFACE_TMP" != "" ]; then
    export KEA_DHCP_INTERFACE="$KEA_DHCP_INTERFACE_TMP"
  fi
}

input_dhcp4_ip () {
  echo -e "What IPv4 address should the DHCP4 server bind to? [Default: $KEA_DHCP4_IP]\n"
  read -rp "Ipv4: " KEA_DHCP4_IP_TMP

  if [ "$KEA_DHCP4_IP_TMP" != "" ]; then
    export KEA_DHCP4_IP="$KEA_DHCP4_IP_TMP"
  fi
}

input_dhcp4_subnet () {
  echo -e "What IPv4 subnet should the DHCP4 server bind to? [Default: $KEA_DHCP4_SUBNET]\n"
  read -rp "CIDR: " KEA_DHCP4_SUBNET_TMP

  if [ "$KEA_DHCP4_SUBNET_TMP" != "" ]; then
    export KEA_DHCP4_SUBNET="$KEA_DHCP4_SUBNET_TMP"
  fi
}

input_dhcp4_gw_ip () {
  echo -e "What is the IPv4 address of the DHCP4 network gateway? [Default: $KEA_DHCP4_GW_IP]\n"
  read -rp "Gateway IPv4: " KEA_DHCP4_GW_IP_TMP

  if [ "$KEA_DHCP4_GW_IP_TMP" != "" ]; then
    export KEA_DHCP4_GW_IP="$KEA_DHCP4_GW_IP_TMP"
  fi
}

# Repeat the same input_dhcp* functions for input_mgmt*

input_mgmt_interface () {
  echo -e "What network interface should be used for container management? [Default: $KEA_MGMT_INTERFACE]\n"
  read -rp "Interface: " KEA_MGMT_INTERFACE_TMP

  if [ "$KEA_MGMT_INTERFACE_TMP" != "" ]; then
    export KEA_MGMT_INTERFACE="$KEA_MGMT_INTERFACE_TMP"
  fi
}

input_mgmt4_ip () {
  echo -e "What IPv4 address should the container bind to for management? [Default: $KEA_MGMT4_IP]\n"
  read -rp "Ipv4: " KEA_MGMT4_IP_TMP

  if [ "$KEA_MGMT4_IP_TMP" != "" ]; then
    export KEA_MGMT4_IP="$KEA_MGMT4_IP_TMP"
  fi
}

input_mgmt4_subnet () {
  echo -e "What IPv4 subnet should be used for the management network? [Default: $KEA_MGMT4_SUBNET]\n"
  read -rp "CIDR: " KEA_MGMT4_SUBNET_TMP

  if [ "$KEA_MGMT4_SUBNET_TMP" != "" ]; then
    export KEA_MGMT4_SUBNET="$KEA_MGMT4_SUBNET_TMP"
  fi
}

input_mgmt4_gw_ip () {
  echo -e "What is the IPv4 address of the management network gateway? [Default: $KEA_MGMT4_GW_IP]\n"
  read -rp "Gateway IPv4: " KEA_MGMT4_GW_IP_TMP

  if [ "$KEA_MGMT4_GW_IP_TMP" != "" ]; then
    export KEA_MGMT4_GW_IP="$KEA_MGMT4_GW_IP_TMP"
  fi
}

input_container_interface () {
  echo -e "What *container* network interface should be used to serve DHCP services? [Default: $KEA_CONTAINER_INTERFACE]\n"
  read -rp "Interface: " KEA_CONTAINER_INTERFACE_TMP

  if [ "$KEA_CONTAINER_INTERFACE_TMP" != "" ]; then
    export KEA_CONTAINER_INTERFACE="$KEA_CONTAINER_INTERFACE_TMP"
  fi
}

input_ha_enabled () {
  echo -e "Would you like to enable HA mode? [Default: $KEA_HA_ENABLED] [Options: yes no]\n"
  read -rp "Enable HA Mode: " KEA_HA_ENABLED_TMP
  KEA_HA_ENABLED_TMP=$(echo "$KEA_HA_ENABLED_TMP" | tr '[:upper:]' '[:lower:]')

  if [ "$KEA_HA_ENABLED_TMP" != "" ]; then
    if ! [[ "$KEA_HA_ENABLED_TMP" =~ ^(yes|no)$ ]]; then
      echo "Invalid response provided for enabling HA mode. Please choose yes or no."
      exit 1
    fi
    KEA_HA_ENABLED="$KEA_HA_ENABLED_TMP"
  fi
}

input_n1_host_ip () {
  echo -e "What IP address would you like to use for the primary HA server? [Default: $KEA_HA_HOST1_IP]\n"
  read -rp "IP: " KEA_HA_HOST1_IP_TMP

  if [ "$KEA_HA_HOST1_IP_TMP" != "" ]; then
    KEA_HA_HOST1_IP="$KEA_HA_HOST1_IP_TMP"
  fi
}

input_n2_host_ip () {
  echo -e "What IP address would you like to use for the secondary DHCP server? [Default: $KEA_HA_HOST2_IP]\n"
  read -rp "IP: " KEA_HA_HOST2_IP_TMP

  if [ "$KEA_HA_HOST2_IP_TMP" != "" ]; then
    KEA_HA_HOST2_IP="$KEA_HA_HOST2_IP_TMP"
  fi
}

input_n_role () {
  echo -e "What role would you like to use for this server? [Default: $KEA_HA_ROLE] [Options: primary secondary]\n"
  read -rp "Role: " KEA_HA_ROLE_TMP
  KEA_HA_ROLE_TMP=$(echo "$KEA_HA_ROLE_TMP" | tr '[:upper:]' '[:lower:]')

  if [ "$KEA_HA_ROLE_TMP" != "" ]; then
    KEA_HA_ROLE="$KEA_HA_ROLE_TMP"
  fi
}

input_env () {
  echo ""
  input_kea_version

  echo ""
  input_kea_log_severity

  echo ""
  input_kea_admin_user

  echo ""
  input_kea_admin_password

  echo ""
  input_db_type

  echo ""
  input_db_version

  echo ""
  input_db_host

  echo ""
  input_db_port

  echo ""
  input_db_user

  echo ""
  input_db_password

  echo ""
  input_db_root_password

  echo ""
  input_db_name

  if [ "$KEA_DB_TYPE" == "postgresql" ]; then
    echo ""
    input_db_schema
  fi

  echo ""
  input_mgmt_interface

  echo ""
  input_mgmt4_ip

  echo ""
  input_mgmt4_subnet

  echo ""
  input_mgmt4_gw_ip

  echo ""
  input_dhcp_interface

  echo ""
  input_dhcp4_ip

  echo ""
  input_dhcp4_subnet

  echo ""
  input_dhcp4_gw_ip

  echo ""
  input_container_interface

  echo ""
  input_ha_enabled

  # Collect additional user input if HA mode is enabled
  if [[ "$KEA_HA_ENABLED" == "yes" ]]; then
    echo ""
    input_n1_host_ip

    echo ""
    input_n2_host_ip

    echo ""
    input_n_role

    process_config
  fi
}
