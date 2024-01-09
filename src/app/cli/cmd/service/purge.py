import click
from loguru import logger
from subprocess import CompletedProcess
from app.cli.cmd.service.down import command as down_command
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from . import group


@group.command('purge')
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool):
    """Purges the entire service deployment. """
    return command(env, yes)


def command(env: Environment, yes: bool) -> CompletedProcess | bool:
    """Purges the entire service deployment. """

    if not yes:
        confirm = click.confirm('Are you sure you want to purge the service deployment?', default=None)

        if not confirm:
            logger.warning('Aborting service deployment purge process for lack of user confirmation or the `-y` flag.')
            return False

    logger.info(f'Purging the service deployment...')

    result = down_command(env, yes, True, '')

    if not result or result.returncode != 0:
        logger.error(f'Failed to purge container services.')
        if result:
            logger.error(result.stderr.decode("utf-8"))
        return False

    logger.success(f'Purged the container services.')
