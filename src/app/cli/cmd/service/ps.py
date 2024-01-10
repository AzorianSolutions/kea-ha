from loguru import logger
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, format_option, all_flag
from ... import Environment
from app.util.console import Run
from . import group, service_argument


@group.command('ps')
@all_flag
@format_option
@service_argument
@pass_environment
def wrapper(env: Environment, all: bool, format: str, service: str):
    """Prints the status of the container processes to the console."""
    return command(env, all, format, service)


def command(env: Environment, all: bool, format: str, service: str) -> CompletedProcess | bool:
    """Prints the status of the container processes to the console."""

    cmd = ['ps']

    if all:
        cmd.append('-a')

    if format:
        cmd.append('--format')
        cmd.append(format)

    if service:
        cmd.append(service)

    result = Run.compose(cmd, env)

    if not result or result.returncode != 0:
        logger.error(f'Could not retrieve container status.')

        if result:
            if stdout := result.stdout.decode("utf-8"):
                logger.debug(stdout)

            if stderr := result.stderr.decode("utf-8"):
                logger.error(stderr)

        return False

    if stdout := result.stdout.decode("utf-8"):
        print(stdout)
