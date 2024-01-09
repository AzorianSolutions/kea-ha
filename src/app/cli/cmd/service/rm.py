import click
from loguru import logger
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.util.console import Run
from . import group, service_argument


@group.command('rm')
@service_argument
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool, service: str):
    """Removes any stopped containers from the service."""
    return command(env, yes, service)


def command(env: Environment, yes: bool, service: str) -> CompletedProcess | bool:
    """Removes any stopped containers from the service."""

    prompt_suffix = f' `{service}`?' if service else 's?'
    log_suffix = f' `{service}`' if service else 's'

    if not yes:
        prompt = f'Are you sure you want to remove the container service{prompt_suffix}'
        confirm = click.confirm(prompt, default=None)

        if not confirm:
            logger.warning('Aborting container service removal process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return False

    prompt = f'Removing the container service{log_suffix}...'
    logger.info(prompt)

    result = Run.compose(['rm'], env)

    if not result or result.returncode != 0:
        logger.error(f'Failed to remove container service{log_suffix}')
        if result:
            logger.error(result.stderr.decode("utf-8"))
            return result
        return False

    logger.success(f'Removed the container service{log_suffix}')

    return result
