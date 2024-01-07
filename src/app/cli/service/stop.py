import click
from loguru import logger
from app.cli.service import group


@group.command('stop')
@click.pass_context
def stop(ctx):
    """Stops the container services."""
    logger.info(f'Stopping the container services...')
