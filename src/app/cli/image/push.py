import click
from loguru import logger
from app.cli.core import Environment
from app.cli.image import group
from app.cli.entry import pass_environment


@group.command('push')
@click.option('-t', '--tag', default='latest', help='The tag to push from the container image.')
@pass_environment
def push(env: Environment, tag: str):
    """Pushes the container image for the given tag."""
    logger.info(f'Pushing the container image; tag: {tag}; debug: {env.settings.debug}')
