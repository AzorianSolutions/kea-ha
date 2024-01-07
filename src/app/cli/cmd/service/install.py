import click
from loguru import logger
from . import group


@group.command('install')
@click.pass_context
def command(ctx):
    """Installs the container services."""
    logger.info(f'Installing the container services...')
