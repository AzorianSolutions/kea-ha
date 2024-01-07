import click
from loguru import logger
from app.cli.entry import pass_environment
from app.model.cli import Environment
from . import group


@group.command('pull')
@click.option('-t', '--tag', default='latest', help='The tag to pull from the container image.')
@pass_environment
def command(env: Environment, tag: str):
    """Pulls the container image for the given tag."""
    logger.info(f'Pulling the container image; tag: {tag}; debug: {env.settings.debug}')
