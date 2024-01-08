import click
import os
from loguru import logger
from pathlib import Path
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.config import ConfigBuilder, ConfigParser
from . import group

HLP_OPT_YES = 'Automatically answer yes to all prompts.'


@group.command('build')
@confirm_option
@pass_environment
def command(env: Environment, yes: bool):
    """Builds the container service files."""

    version: str = env.settings.c('kea/version')

    if not yes:
        confirm = click.confirm('Are you sure you want to build the container service files?', default=None)

        if not confirm:
            logger.warning('Aborting container service file build process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return

        click.echo('What version of the Kea software would you like to deploy?\n')

        version_input = click.prompt('Kea Version', default=env.settings.c('kea/version'))

        if version_input and version_input != version:
            version = version_input

            # Save the version change back to the configuration
            env.settings.u('kea/version', version)
            env.settings.save()

    env_file = Path(env.settings.c('service/paths/compose/env'))

    # Save the service environment file if the path is writable
    if env_file.exists() and not os.access(env_file, os.W_OK):
        logger.error(f'No write permission to existing environment file: {env_file}')
        return

    # Build the services environment file
    file_contents = ConfigBuilder.build_env_file(env.settings.config)

    with open(env_file, 'w') as f:
        f.write(file_contents)
        f.close()

    logger.info(f'Saved the service environment file: {env_file}')

    compose_tpl_path = f'src/tpl/docker/docker-compose-{env.settings.c("kea/backend/type")}.yml'

    # Render the configuration file template
    try:
        template = ConfigBuilder.build_tpl(compose_tpl_path, env.settings.config)
    except FileNotFoundError as e:
        logger.error(f'Failed to find the compose file template: {compose_tpl_path}')
        return

    compose_file = Path(env.settings.c('service/paths/compose/file'))

    with open(compose_file, 'w') as f:
        f.write(template)
        f.close()

    logger.info(f'Saved the service compose file: {compose_file}')

    templates = [
        'kea-ctrl-agent',
        'kea-dhcp4',
        # 'kea-dhcp6',
        'supervisor-kea-ctrl-agent',
        'supervisor-kea-dhcp4',
        # 'supervisor-kea-dhcp6',
        'supervisord',
    ]

    for tpl_name in templates:
        conf_tpl_path = f'src/tpl/conf/{tpl_name}.conf'
        conf_tpl_ref = tpl_name.replace('-', '_')

        # Render the configuration file template
        try:
            template = ConfigBuilder.build_tpl(conf_tpl_path, env.settings.config)
        except FileNotFoundError as e:
            logger.error(f'Failed to find the conf file template: {conf_tpl_path}')
            return

        conf_file = Path(env.settings.c(f'service/paths/conf/{conf_tpl_ref}'))

        if not conf_file.parent.exists():
            logger.debug(f'Creating the service conf file directory: {conf_file.parent}')
            conf_file.parent.mkdir(parents=True)

        with open(conf_file, 'w') as f:
            f.write(template)
            f.close()

        logger.debug(f'Saved the service conf file: {conf_file}')

    logger.success('Successfully built the container service files.')