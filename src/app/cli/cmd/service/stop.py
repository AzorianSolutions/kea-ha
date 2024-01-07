import click
from loguru import logger
from . import group


@group.command('stop')
@click.pass_context
def command(ctx):
    """Stops the container services."""
    logger.info(f'Stopping the container services...')
