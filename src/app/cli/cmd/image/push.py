import click
from loguru import logger
from app.cli.entry import pass_environment
from app.model.cli import Environment
from . import group


@group.command('push')
@click.option('-t', '--tag', default='latest', help='The tag to push from the container image.')
@pass_environment
def command(env: Environment, tag: str):
    """Pushes the container image for the given tag."""
    logger.info(f'Pushing the container image; tag: {tag}; debug: {env.settings.debug}')
