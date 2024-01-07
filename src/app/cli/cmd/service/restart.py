import click
from loguru import logger
from . import group


@group.command('restart')
@click.pass_context
def command(ctx):
    """Restarts the container services."""
    logger.info(f'Restarting the container services...')
