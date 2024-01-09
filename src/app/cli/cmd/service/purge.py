import click
from loguru import logger
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from . import group


@group.command('purge')
@confirm_option
@pass_environment
def command(env: Environment, yes: bool):
    """Purges the entire service deployment. """

    if not yes:
        confirm = click.confirm('Are you sure you want to purge the service deployment?', default=None)

        if not confirm:
            logger.warning('Aborting service deployment purge process for lack of user confirmation or the `-y` flag.')
            return

    logger.info(f'Purging the service deployment...')
    logger.warning('Feature not implemented!')
