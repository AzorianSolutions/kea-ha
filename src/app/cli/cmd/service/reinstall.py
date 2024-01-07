import click
from loguru import logger
from app.cli.cmd.service import group


@group.command('reinstall')
@click.pass_context
def reinstall(ctx):
    """Re-Installs the container services."""
    logger.info(f'Re-Installing the container services...')
