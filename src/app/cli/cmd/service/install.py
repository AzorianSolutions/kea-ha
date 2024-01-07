import click
from loguru import logger
from app.cli.cmd.service import group


@group.command('install')
@click.pass_context
def install(ctx):
    """Installs the container services."""
    logger.info(f'Installing the container services...')
