import click
from loguru import logger
from app.cli.core import Environment
from app.cli.image import group
from app.cli.entry import pass_environment


@group.command('purge')
@click.option('-t', '--tag', default=None, help='The tag to purge from the container image.')
@pass_environment
def purge(env: Environment, tag: str):
    """Purges the entire container image or just the given tag."""
    logger.info(f'Purging the container image; tag: {tag}; debug: {env.settings.debug}')
