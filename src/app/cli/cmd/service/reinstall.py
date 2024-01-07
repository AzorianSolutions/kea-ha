import click
from loguru import logger
from . import group


@group.command('reinstall')
@click.pass_context
def command(ctx):
    """Re-Installs the container services."""
    logger.info(f'Re-Installing the container services...')
