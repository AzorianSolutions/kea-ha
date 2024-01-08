import click
from loguru import logger
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.console import Run
from . import group


@group.command('install')
@confirm_option
@pass_environment
def command(env: Environment, yes: bool):
    """Installs the container services."""

    version: str = env.settings.c('kea/version')

    if not yes:
        confirm = click.confirm('Are you sure you want to install the container services?', default=None)

        if not confirm:
            logger.warning('Aborting container service installation process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return

        click.echo('What version of the Kea software would you like to deploy?\n')

        version_input = click.prompt('Kea Version', default=env.settings.c('kea/version'))

        if version_input and version_input != version:
            version = version_input

            # Save the version change back to the configuration
            env.settings.u('kea/version', version)
            env.settings.save()

    logger.info(f'Installing the container services...')

    result = Run.compose(['up', '-d'], env)

    if not result or result.returncode != 0:
        logger.error(f'Container services installation failed.')

        if result:
            logger.error(result.stderr.decode("utf-8"))

        return

    logger.success(f'Installed the container services.')
