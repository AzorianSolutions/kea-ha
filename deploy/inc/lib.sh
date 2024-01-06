#!/usr/bin/env bash

ROOT_PATH="$(cd "$(dirname "$0")" || exit; pwd)"

contains() {
    [[ $1 =~ (^|[[:space:]])$2($|[[:space:]]) ]] && exit 0 || exit 1
}

clean_build () {
  # Remove the service configuration and Docker files, leaving the environment configuration file
  rm -fr build/docker/*.yml
}

process_config () {
  if [ "$KEA_HA_ROLE" == "primary" ]; then
    # shellcheck disable=SC2034
    export KEA_HA_HOST_NAME="node1"
    # shellcheck disable=SC2153
    export KEA_HA_HOST_IP="$KEA_HA_HOST1_IP"
  elif [ "$KEA_HA_ROLE" == "secondary" ]; then
    # shellcheck disable=SC2034
    export KEA_HA_HOST_NAME="node2"
    # shellcheck disable=SC2153,SC2034
    export KEA_HA_HOST_IP="$KEA_HA_HOST2_IP"
  fi
}

load_env_default () {
  # Load the user's environment configuration into the shell
  # shellcheck disable=SC2046
  export $(grep -v '^#' defaults.env | xargs)

  # Populate environment variables based on the current input
  process_config
}

load_env_config () {
  # Load the user's environment configuration into the shell if it exists
  if [ -f "build/docker/.env" ]; then
    # shellcheck disable=SC2046
    export $(grep -v '^#' build/docker/.env | xargs)
  fi

  # Populate environment variables based on the current input
  process_config
}

build_env_config () {
  # Create associated build directory if it doesn't exist
  mkdir -p "build/docker"

  # Remove the existing Docker environment file if it exists
  if [ -f "build/docker/.env" ]; then
    rm -fr "build/docker/.env"
  fi

  # Build the environment file from the template
  envsubst < "deploy/tpl/.env" > "build/docker/.env"
}

compose_command () {
  # Check if Docker Compose file exists and is readable
  if [ ! -r "build/docker/docker-compose.yml" ]; then
    echo "Docker Compose file build/docker/docker-compose.yml does not exist or is not readable"
    exit 1
  fi

  # shellcheck disable=SC2086
  docker compose --project-directory "$ROOT_PATH" --env-file build/docker/.env -f "build/docker/docker-compose.yml" $1
}

build_docker_compose () {
  source_path="deploy/docker/docker-compose-${KEA_DB_TYPE}.yml"
  docker_path="build/docker"
  compose_path="${docker_path}/docker-compose.yml"

  # Create associated build directory if it doesn't exist
  if [ ! -d "$docker_path" ]; then
    mkdir -p "$docker_path"
  fi

  # Remove the existing Docker Compose file if it exists
  if [ -f "$compose_path" ]; then
    rm -fr "$compose_path"
  fi

  # Create the Docker Compose file from the template
  cp -Ra "$source_path" "$compose_path"
}

build_image () {
  TAG="latest"

  if [ "$1" != "" ]; then
    TAG="$1"
  elif [ "$KEA_IMAGE_TAG" != "" ]; then
    TAG="$KEA_IMAGE_TAG"
  fi

  export DOCKER_BUILDKIT=1

  # shellcheck disable=SC2153
  docker build \
          -t "${KEA_IMAGE_REPO_URL}/${KEA_IMAGE_REPO_USERNAME}/${KEA_IMAGE_NAME}:${TAG}" \
          -f deploy/docker/Dockerfile .\
          --build-arg KHA_VERSION="${KHA_VERSION}" \
          --build-arg KHA_SHARE_PATH="${KHA_SHARE_PATH}" \
          --build-arg KEA_VERSION="${KEA_VERSION}"
}

tag_image () {
  TAG="latest"
  TARGET="latest"

  if [ "$1" != "" ]; then
    TAG="$1"
  elif [ "$KEA_IMAGE_TAG" != "" ]; then
    TAG="$KEA_IMAGE_TAG"
  fi

  if [ "$2" != "" ]; then
    TARGET="$2"
  fi

  # shellcheck disable=SC2153
  docker tag "${KEA_IMAGE_REPO_URL}/${KEA_IMAGE_REPO_USERNAME}/${KEA_IMAGE_NAME}:${TAG}" "${KEA_IMAGE_REPO_URL}/${KEA_IMAGE_REPO_USERNAME}/${KEA_IMAGE_NAME}:${TARGET}"
}

push_image () {
  TAG="latest"

  if [ "$1" != "" ]; then
    TAG="$1"
  elif [ "$KEA_IMAGE_TAG" != "" ]; then
    TAG="$KEA_IMAGE_TAG"
  fi

  # shellcheck disable=SC2153
  docker push "${KEA_IMAGE_REPO_URL}/${KEA_IMAGE_REPO_USERNAME}/${KEA_IMAGE_NAME}:${TAG}"
}
