from loguru import logger
from app.cli.cmd.service.install import command as install_command
from app.cli.cmd.service.uninstall import command as uninstall_command
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from . import group


@group.command('reinstall')
@confirm_option
@pass_environment
def command(env: Environment, yes: bool):
    """Re-Installs the container services."""

    logger.info(f'Re-Installing the container services...')

    uninstall_command(env, yes)
    install_command(env, yes)
