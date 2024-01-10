import click
import os
from loguru import logger
from pathlib import Path
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, confirm_option
from ... import Environment
from app.util.config import ConfigBuilder
from . import group


@group.command('clean')
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool):
    """Cleans the container service build path."""
    return command(env, yes)


def command(env: Environment, yes: bool) -> CompletedProcess | bool:
    """Cleans the container service build path."""

    if not yes:
        confirm = click.confirm('Are you sure you want to clean the container service build path?', default=None)

        if not confirm:
            logger.warning('Aborting container service build path cleaning process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return False

    compose_file = Path(str(env.config('service/paths/compose/file')))
    env_file = Path(str(env.config('service/paths/compose/env')))

    if compose_file.exists():
        os.remove(compose_file)
        logger.debug(f'Removed compose file: {compose_file}')

    if env_file.exists():
        os.remove(env_file)
        logger.debug(f'Removed env file: {env_file}')

    logger.success('Successfully cleaned the container service build path.')
