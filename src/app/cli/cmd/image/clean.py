import click
import os
from loguru import logger
from pathlib import Path
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from . import group


@group.command('clean')
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool):
    """Cleans the image build path."""
    return command(env, yes)


def command(env: Environment, yes: bool) -> CompletedProcess | bool:
    """Cleans the image build path."""

    if not yes:
        confirm = click.confirm('Are you sure you want to clean the image build path?', default=None)

        if not confirm:
            logger.warning('Aborting image build path cleaning process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return False

    build_path = Path(str(env.config('service/paths/kha/root')))
    dockerfile = Path(str(env.config('image/build/dockerfile')))
    dockerignore_file = build_path / '.dockerignore'
    entrypoint_file = build_path / 'entrypoint.sh'

    if dockerfile.exists():
        os.remove(dockerfile)
        logger.debug(f'Removed Dockerfile: {dockerfile}')

    if dockerignore_file.exists():
        os.remove(dockerignore_file)
        logger.debug(f'Removed .dockerignore file: {dockerignore_file}')

    if entrypoint_file.exists():
        os.remove(entrypoint_file)
        logger.debug(f'Removed entrypoint script: {entrypoint_file}')

    logger.success('Successfully cleaned the image build path.')
