import click
from loguru import logger
from subprocess import CompletedProcess
from app.cli.entry import pass_environment, confirm_option
from ... import Environment
from app.util.console import Run
from . import group, service_argument


@group.command('up')
@service_argument
@confirm_option
@pass_environment
def wrapper(env: Environment, yes: bool, service: str):
    """Installs the container services."""
    return command(env, yes, service)


def command(env: Environment, yes: bool, service: str) -> CompletedProcess | bool:
    """Installs the container services."""

    prompt_suffix = f' `{service}`?' if service else 's?'
    log_suffix = f' `{service}`' if service else 's'

    version: str = env.config('kea/version')

    if not yes:
        prompt = f'Are you sure you want to install the container service{prompt_suffix}'
        confirm = click.confirm(prompt, default=None)

        if not confirm:
            logger.warning('Aborting container service installation process for lack of user confirmation '
                           + 'or the `-y` flag.')
            return False

        click.echo('What version of the Kea software would you like to deploy?\n')

        version_input = click.prompt('Kea Version', default=env.config('kea/version'))

        if version_input and version_input != version:
            version = version_input

            # Save the version change back to the configuration
            env.config.kea.version = version
            env.save()

    logger.info(f'Installing the container service{log_suffix}...')

    result = Run.compose(['up', '-d'], env)

    if not result or result.returncode != 0:
        logger.error(f'Failed installation for container service{log_suffix}')
        if result:
            logger.error(result.stderr.decode("utf-8"))
            return result
        return False

    logger.success(f'Installed the container service{log_suffix}')

    return result
