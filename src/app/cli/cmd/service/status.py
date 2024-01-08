from loguru import logger
from app.cli.entry import pass_environment
from app.model.cli import Environment
from app.util.console import Run
from . import group


def command(env: Environment):
    """Prints the status of the containers to the console."""

    result = Run.compose(['ps'], env)

    if not result or result.returncode != 0:
        logger.error(f'Could not retrieve container status.')
        if result:
            logger.error(result.stderr.decode("utf-8"))
        return
    else:
        print(result.stdout.decode("utf-8"))


@group.command('status')
@pass_environment
def wrapper(env: Environment):
    """Prints the status of the containers to the console."""
    return command(env)
