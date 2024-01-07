import click
from loguru import logger
from app.cli.service import group


@group.command('status')
@click.pass_context
def status(ctx):
    """Prints the container statuses."""
    logger.info(f'Printing the container statuses.')
