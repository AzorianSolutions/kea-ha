import click
from loguru import logger
from app.model.cli import Environment
from app.cli.cmd.image import group

import app
from app.cli.entry import pass_environment


@group.command('pull')
@click.option('-t', '--tag', default='latest', help='The tag to pull from the container image.')
@pass_environment
def pull(env: Environment, tag: str):
    """Pulls the container image for the given tag."""
    logger.info(f'Pulling the container image; tag: {tag}; debug: {app.settings.debug}')
