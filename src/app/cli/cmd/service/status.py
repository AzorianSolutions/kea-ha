import click
from loguru import logger
from . import group


@group.command('status')
@click.pass_context
def command(ctx):
    """Prints the container statuses."""
    logger.info(f'Printing the container statuses.')
