import click
from loguru import logger
from app.cli.entry import pass_environment
from app.model.cli import Environment
from . import group


@group.command('build')
@click.option('-t', '--tag', default='latest', help='The tag to use for the container image.')
@pass_environment
def command(env: Environment, tag: str):
    """Builds the container image for the given tag."""
    logger.info(f'Building the container image; tag: {tag}; debug: {env.settings.debug}')
