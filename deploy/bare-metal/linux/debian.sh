#!/usr/bin/env bash

root_path=$(pwd)

source_path=${1:-$root_path/defaults.env}
install_packages=${2:-}
install_venv=${3:-}

system_packages='build-essential,python3,python3-dev,python3-pip,python3-venv'

system_packages=$(echo "$system_packages" | tr ',' ' ')

# shellcheck source=defaults.env
source "$source_path"

if [ "$install_packages" == "" ]; then
    read -rp "Do you want to install the required system packages for this project? [y/n] " install_packages
fi

install_packages=$(echo "$install_packages" | tr '[:upper:]' '[:lower:]')

case "$install_packages" in
    1|t|true|y|yes|yeah|yep|sure)
        install_packages="1"
        ;;
    *)
        ;;
esac

if [ "$install_packages" == "1" ]; then
    echo "Installing system packages..."
    sudo apt update
    # shellcheck disable=SC2086
    sudo apt-get -y --ignore-missing install $system_packages
fi

if [ "$install_venv" == "" ]; then
    echo ""
    read -rp "Do you want to install the Python virtual environment and install pip dependencies? [y/n] " install_venv
fi

install_venv=$(echo "$install_venv" | tr '[:upper:]' '[:lower:]')

case "$install_venv" in
    1|t|true|y|yes|yeah|yep|sure)
        install_venv="1"
        ;;
    *)
        ;;
esac

if [ "$install_venv" == "1" ]; then
    echo ""
    echo "Installing Python virtual environment and pip dependencies..."
    rm -fr venv
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
fi
