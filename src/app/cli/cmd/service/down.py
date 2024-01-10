import click
from loguru import logger
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, confirm_option
from ... import Environment
from app.util.console import Run
from . import group, service_argument


@group.command('down')
@confirm_option
@click.option('-v', '--volumes', is_flag=True, default=False, help='Remove associated volumes.')
@service_argument
@pass_environment
def wrapper(env: Environment, yes: bool, volumes: bool, service: str):
    """Stops and removes all service containers, and optionally removes any volumes associated with the service."""
    return command(env, yes, volumes, service)


def command(env: Environment, yes: bool, volumes: bool, service: str) -> CompletedProcess | bool:
    """Stops and removes all service containers, and optionally removes any volumes associated with the service."""

    prompt_suffix = f' `{service}`?' if service else 's?'
    log_suffix = f' `{service}`' if service else 's'

    if not yes:
        prompt = f'Are you sure you want to stop and remove the container service{prompt_suffix}'
        confirm = click.confirm(prompt, default=None)

        if not confirm:
            logger.warning('Aborting container service removal process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return False

    prompt = f'Stopping and removing the container service{log_suffix}...'
    logger.info(prompt)

    cmd = ['down']

    if volumes:
        cmd.append('-v')

    result = Run.compose(cmd, env)

    if not result or result.returncode != 0:
        logger.error(f'Failed to stop and remove container service{log_suffix}.')
        if result:
            logger.error(result.stderr.decode("utf-8"))
            return result
        return False

    logger.success(f'Stopped and removed the container service{log_suffix}.')

    return result
