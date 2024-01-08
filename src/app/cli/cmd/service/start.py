import click
from loguru import logger
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.console import Run
from . import group


def command(env: Environment, yes: bool):
    """Starts the container services."""

    if not yes:
        confirm = click.confirm('Are you sure you want to start the container services?', default=None)

        if not confirm:
            logger.warning('Aborting container service start process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return

    logger.info(f'Starting the container services...')

    result = Run.compose(['start'], env)

    if not result or result.returncode != 0:
        logger.error(f'Container services start failed.')
        if result:
            logger.error(result.stderr.decode("utf-8"))
        return

    logger.success(f'Started the container services.')


@group.command('start')
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool):
    """Starts the container services."""
    return command(env, yes)
