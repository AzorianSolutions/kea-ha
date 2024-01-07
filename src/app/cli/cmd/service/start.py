import click
from loguru import logger
from app.cli.cmd.service import group


@group.command('start')
@click.pass_context
def start(ctx):
    """Starts the container services."""
    logger.info(f'Starting the container services...')
