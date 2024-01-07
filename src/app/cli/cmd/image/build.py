import click
from loguru import logger
from app.model.cli import Environment
from app.cli.cmd.image import group

import app
from app.cli.entry import pass_environment


@group.command('build')
@click.option('-t', '--tag', default='latest', help='The tag to use for the container image.')
@pass_environment
def build(env: Environment, tag: str):
    """Builds the container image for the given tag."""
    logger.info(f'Building the container image; tag: {tag}; debug: {app.settings.debug}')