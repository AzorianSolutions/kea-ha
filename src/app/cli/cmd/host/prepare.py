import json
import os
from loguru import logger
from pathlib import Path
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.console import Run
from . import group

docker_config: dict = {
    'bip': '192.168.228.1/23',
    'default-address-pools': [{'base': '192.168.230.0/23', 'size': 27}],
    'features': {'buildkit': True},
}


@group.command('prepare')
@confirm_option
@pass_environment
def command(env: Environment, yes: bool):
    """Prepares the host environment to run the service containers."""
    logger.info(f'Preparing the host environment for service containers; confirmed: {yes}; debug: {env.settings.debug}')

    # Update the APT cache
    process = Run.c(['sudo', 'apt-get', 'update', '-y' if yes else ''])

    if process.returncode != 0:
        logger.warning(f'APT update yielded errors: {process.stderr}')

    # Upgrade the host environment
    process = Run.c(['sudo', 'apt-get', 'upgrade', '-y' if yes else ''])

    if process.returncode != 0:
        logger.error(f'Failed to perform a upgrade on the host environment: {process.stderr}')
        if env.debug:
            logger.info(process.stdout)
        return

    prepare_packages = env.settings.c('host/packages/prepare')

    # Install the prepare-stage packages
    process = Run.c(['sudo', 'apt-get', 'install', '-y' if yes else '', *prepare_packages.split(' ')])

    if process.returncode != 0:
        logger.error(f'Failed to install first-stage APT packages in the host environment: {process.stderr}')
        if env.debug:
            logger.info(process.stdout)
        return

    docker_keyring: Path = Path('/usr/share/keyrings/docker-archive-keyring.gpg')

    if not docker_keyring.exists():
        logger.info(f'Installing Docker keyring...')

        # Install the Docker keyring
        process = Run.c(['curl', '-fsSL', 'https://download.docker.com/linux/ubuntu/gpg', '|', 'sudo', 'gpg', '--dearmor', '-o', docker_keyring])

        if process.returncode != 0:
            logger.error(f'Failed to install Docker keyring: {process.stderr}')
            if env.debug:
                logger.info(process.stdout)
            return

    apt_sources: Path = Path('/etc/apt/sources.list.d/docker.list')

    if not apt_sources.exists():
        logger.info(f'Installing Docker APT sources...')

        # Install the Docker APT sources
        process = Run.c(['echo', '"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu', '$(lsb_release -cs) stable"', '|', 'sudo', 'tee', apt_sources])

        if process.returncode != 0:
            logger.error(f'Failed to install Docker APT sources: {process.stderr}')
            if env.debug:
                logger.info(process.stdout)
            return

    # Update the APT cache
    process = Run.c(['sudo', 'apt-get', 'update', '-y' if yes else ''])

    if process.returncode != 0:
        logger.warning(f'APT update yielded errors: {process.stderr}')

    payload_packages = env.settings.c('host/packages/payload')

    # Install the payload packages
    process = Run.c(['sudo', 'apt-get', 'install', '-y' if yes else '', *payload_packages.split(' ')])

    if process.returncode != 0:
        logger.error(f'Failed to install first-stage APT packages in the host environment: {process.stderr}')
        if env.debug:
            logger.info(process.stdout)
        return

    docker_config_path: Path = Path('/etc/docker/daemon.json')

    if not docker_config_path.exists():
        # Configure the Docker daemon
        with open(docker_config_path, 'w') as file:
            file.write(json.dumps(docker_config, indent=4))

    elif env.debug:
        logger.debug(f'Docker daemon configuration already exists at {docker_config_path}.')

    # Restart the Docker daemon
    process = Run.c(['sudo', 'systemctl', 'restart', 'docker'])

    if process.returncode != 0:
        logger.error(f'Failed to restart Docker daemon: {process.stderr}')
        if env.debug:
            logger.info(process.stdout)

    # Install the Docker daemon service
    process = Run.c(['sudo', 'systemctl', 'enable', 'docker'])

    if process.returncode != 0:
        logger.error(f'Failed to enable Docker daemon service: {process.stderr}')
        if env.debug:
            logger.info(process.stdout)

    # Add the current user to the Docker group
    process = Run.c(['sudo', 'adduser', os.getlogin(), 'docker'])

    if process.returncode != 0:
        logger.error(f'Failed to add current user to Docker group: {process.stderr}')
        if env.debug:
            logger.info(process.stdout)

    logger.success(f'Host environment prepared for service containers.')
