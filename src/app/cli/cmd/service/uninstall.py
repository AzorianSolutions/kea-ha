import click
from loguru import logger
from app.cli.cmd.service import group


@group.command('uninstall')
@click.pass_context
def uninstall(ctx):
    """Uninstalls the container services."""
    logger.info(f'Uninstalling the container services...')
