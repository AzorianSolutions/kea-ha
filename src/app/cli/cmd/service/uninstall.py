import click
from loguru import logger
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.console import Run
from . import group


def command(env: Environment, yes: bool):
    """Uninstalls the container services."""

    if not yes:
        confirm = click.confirm('Are you sure you want to uninstall the container services?', default=None)

        if not confirm:
            logger.warning('Aborting container service uninstallation process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return

    logger.info(f'Uninstalling the container services...')

    result = Run.compose(['down'], env)
    result2 = Run.compose(['rm'], env)

    if not result or result.returncode != 0 or not result2 or result2.returncode != 0:
        logger.error(f'Container services uninstallation failed.')
        if result:
            logger.error(result.stderr.decode("utf-8"))
        return

    logger.success(f'Uninstalled the container services.')


@group.command('uninstall')
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool):
    """Installs the container services."""
    return command(env, yes)
