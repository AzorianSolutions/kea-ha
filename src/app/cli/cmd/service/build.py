import click
import os
from loguru import logger
from pathlib import Path
from app.cli.entry import pass_environment
from app.model.cli import Environment
from app.util.config import ConfigBuilder
from . import group

HLP_OPT_YES = 'Automatically answer yes to all prompts.'


@group.command('build')
@click.option('-y', '--yes', is_flag=True, default=False, help=HLP_OPT_YES)
@pass_environment
def command(env: Environment, yes: bool):
    """Builds the container service files."""

    version: str = env.settings.c('kea__version')

    if not yes:
        confirm = click.confirm('Are you sure you want to build the container service files?', default=None)

        if not confirm:
            logger.warning('Aborting container service file build process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return

        click.echo('What version of the Kea software would you like to deploy?\n')

        version_input = click.prompt('Kea Version', default=env.settings.c('kea__version'))

        if version_input and version_input != version:
            version = version_input

            # Save the version change back to the configuration
            env.settings.u('kea__version', version)
            env.settings.save()

    env_file = Path(env.settings.c('service__environment__file'))

    # Save the service environment file if the path is writable
    if not os.access(env_file, os.W_OK):
        logger.error(f'Failed to write the service environment file: {env_file}')
        return

    # Build the service environment file
    file_contents = ConfigBuilder.build_env_file(env.settings.config)

    with open(env_file, 'w') as f:
        f.write(file_contents)
        f.close()

    logger.success(f'Saved the service environment file: {env_file}')
