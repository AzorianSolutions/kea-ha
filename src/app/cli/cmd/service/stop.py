import click
from loguru import logger
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.console import Run
from . import group


@group.command('stop')
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool):
    """Stops the container services."""
    return command(env, yes)


def command(env: Environment, yes: bool) -> CompletedProcess | bool:
    """Stops the container services."""

    if not yes:
        confirm = click.confirm('Are you sure you want to stop the container services?', default=None)

        if not confirm:
            logger.warning('Aborting container service stop process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return False

    logger.info(f'Stopping the container services...')

    result = Run.compose(['stop'], env)

    if not result or result.returncode != 0:
        logger.error(f'Container services stop failed.')
        if result:
            logger.error(result.stderr.decode("utf-8"))
            return result
        return False

    logger.success(f'Stopped the container services.')

    return result
