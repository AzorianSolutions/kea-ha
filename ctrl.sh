#!/usr/bin/env bash

# Load custom libraries
source deploy/inc/lib.sh
source deploy/inc/input.sh

# Load the default environment configuration into the shell
load_env_default

action=${1:-}
intact=${2:-1}

# Confirm with the user what action to take if not provided
input_action

action_configure () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Load the default environment configuration into the shell
  load_env_default

  # Load the environment configuration into the shell
  load_env_config

  # Prompt the user to configure the environment if required
  if [ "$interactive" == "1" ]; then
    input_env
  fi

  # Update the environment configuration with the user's input
  build_env_config
}

action_prepare () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Confirm that the user wants to prepare the system
  if [ "$interactive" == "1" ]; then
    input_confirm_action "prepare"
  fi

  sudo apt update && sudo apt dist-upgrade -y
  sudo apt install -y ca-certificates curl gnupg lsb-release

  # Download Docker GPG key and add it to the keyring if it doesn't already exist
  if [ ! -f /usr/share/keyrings/docker-archive-keyring.gpg ]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  fi

  # Add the Docker repository to the APT sources if it doesn't already exist
  if [ ! -f /etc/apt/sources.list.d/docker.list ]; then
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  fi

  # Update APT and install Docker
  sudo apt update
  sudo apt install -y docker-ce docker-ce-cli containerd.io net-tools

  # Reconfigure Docker networking to a non-conflicting subnet if a configuration file doesn't already exist
  if [ ! -f /etc/docker/daemon.json ]; then
    echo '{
  "bip": "192.168.228.1/23",
  "default-address-pools": [{"base":"192.168.230.0/23","size":27}]
}
' | sudo tee /etc/docker/daemon.json > /dev/null
  fi

  # Restart Docker
  sudo systemctl restart docker

  # Add the current user to the Docker group
  sudo adduser "$USER" docker
}

action_build () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  version=${2:-}

  # Load the environment configuration
  load_env_config

  # Prompt the user to configure the Kea version if not provided
  if [ "$interactive" == "1" ] && [ "$version" == "" ]; then
    # Prompt the user to configure the Kea version
    input_kea_version
  elif [ "$version" == "" ]; then
    # Set the version to the default value
    version="${KEA_VERSION}"
  else
    # Set the Kea version to the provided value
    export KEA_VERSION="$version"
  fi

  # Build the environment configuration to save potentially changed Kea version
  build_env_config

  # Build the Docker image
  build_image "${KEA_VERSION}"
}

action_push () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Load the environment configuration
  load_env_config

  # Push the container image to a container repository
  push_image "${KEA_IMAGE_TAG}"
}

action_install () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Load the environment configuration into the shell
  load_env_config

  if [ "$interactive" == "1" ]; then
    input_confirm_action "install"

    action_configure

    # Update the environment configuration with potential user changes
    build_env_config
  fi

  # Clean build files
  clean_build

  # Build the Docker Compose files
  build_docker_compose

  # Create/Update/Start the Docker service containers
  compose_command "up -d"
}

action_uninstall () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Load the environment configuration into the shell
  load_env_config

  if [ "$interactive" == "1" ]; then
    input_confirm_action "uninstall"
  fi

  # Stop the Docker services and remove the containers
  compose_command "down"
  compose_command "rm"

  # Clean the build files
  clean_build
}

action_reinstall () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Uninstall the container services
  action_uninstall "$interactive"

  # Reinstall the services
  action_install "$interactive"
}

action_purge () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Load the environment configuration into the shell
  load_env_config

  # Confirm that the user wants to purge the services
  if [ "$interactive" == "1" ]; then
    input_confirm_action "purge"
  fi

  # Uninstall the container services
  action_uninstall "$interactive"

  # Remove the build files
  rm -fr build

  # Remove the Docker images
  docker rmi "${KEA_IMAGE_REPO_USERNAME}/${KEA_IMAGE_NAME}"

  # Purge Docker build cache
  docker builder prune -a -f
}

action_update () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Load the environment configuration into the shell
  load_env_config

  # Confirm that the user wants to update the services
  if [ "$interactive" == "1" ]; then
    input_confirm_action "update"

    # Prompt the user to configure the Kea version
    input_kea_version

    # Build the environment configuration with potentially changed Kea version
    build_env_config
  fi

  echo ""
  echo "Updating to Kea version $KEA_VERSION"
  echo ""

  # Reinstall the services
  action_reinstall "$interactive"
}

action_start () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Confirm that the user wants to start the services
  if [ "$interactive" == "1" ]; then
    input_confirm_action "start"
  fi

  # Start the Docker services
  compose_command "start"
}

action_stop () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Confirm that the user wants to stop the services
  if [ "$interactive" == "1" ]; then
    input_confirm_action "stop"
  fi

  # Stop the Docker services
  compose_command "stop"
}

action_restart () {
  interactive=0
  if [ "$1" == "1" ]; then
    interactive=1
  fi

  # Confirm that the user wants to restart the services
  if [ "$interactive" == "1" ]; then
    input_confirm_action "restart"
  fi

  # Restart the Docker services
  compose_command "restart"
}

action_status () {
  # Display the Docker service status
  compose_command "ps"
}

action_version () {
  # Display the Kea HA tool version
  # shellcheck disable=SC2153
  echo "Kea HA Tool Version: ${KHA_VERSION}"
}

# Run the appropriate action
if [ "$action" == "configure" ]; then

  action_configure "$intact"

elif [ "$action" == "prepare" ]; then

  action_prepare "$intact"

elif [ "$action" == "build" ]; then

  action_build "$intact"

elif [ "$action" == "push" ]; then

  action_push "$intact"

elif [ "$action" == "install" ]; then

  # Prompt the user to configure the environment
  action_configure

  # Install the services interactively
  action_install "$intact"

elif [ "$action" == "uninstall" ]; then

  action_uninstall "$intact"

elif [ "$action" == "reinstall" ]; then

  action_reinstall "$intact"

elif [ "$action" == "purge" ]; then

  action_purge "$intact"

elif [ "$action" == "update" ]; then

  action_update "$intact"

elif [ "$action" == "start" ]; then

  action_start "$intact"

elif [ "$action" == "stop" ]; then

  action_stop "$intact"

elif [ "$action" == "restart" ]; then

  action_restart "$intact"

elif [ "$action" == "status" ]; then

  action_status

elif [ "$action" == "version" ]; then

  action_version

elif [ "$action" == "exit" ]; then

  exit 0

# Handle invalid actions
else

  printf 'Invalid action: %s\n' "$action"
  exit 1

fi

# Default exit path
exit 0