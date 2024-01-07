import click
from loguru import logger
from . import group


@group.command('start')
@click.pass_context
def command(ctx):
    """Starts the container services."""
    logger.info(f'Starting the container services...')
