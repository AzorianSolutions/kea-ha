import click
from loguru import logger
from . import group


@group.command('uninstall')
@click.pass_context
def command(ctx):
    """Uninstalls the container services."""
    logger.info(f'Un-Installing the container services...')
