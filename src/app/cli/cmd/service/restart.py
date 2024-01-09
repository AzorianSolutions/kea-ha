import click
from loguru import logger
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.console import Run
from . import group


@group.command('restart')
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool):
    """Restarts the container services."""
    return command(env, yes)


def command(env: Environment, yes: bool) -> CompletedProcess | bool:
    """Restarts the container services."""

    if not yes:
        confirm = click.confirm('Are you sure you want to restart the container services?', default=None)

        if not confirm:
            logger.warning('Aborting container service restart process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return False

    logger.info(f'Restarting the container services...')

    result = Run.compose(['restart'], env)

    if not result or result.returncode != 0:
        logger.error(f'Container services restart failed.')
        if result:
            logger.error(result.stderr.decode("utf-8"))
            return result
        return False

    logger.success(f'Restarted the container services.')

    return result
