import click
from loguru import logger
from app.cli.cmd.service import group


@group.command('restart')
@click.pass_context
def restart(ctx):
    """Restarts the container services."""
    logger.info(f'Restarting the container services...')
