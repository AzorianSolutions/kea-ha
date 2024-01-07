import click
from app import settings
from app.model.cli import Environment

pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group()
@click.version_option(settings.version, '-V', '--version', message='%(version)s')
@click.option('-d', '--debug', default=settings.debug, is_flag=True, help='Enables debug mode.')
@pass_environment
def cli(env: Environment, debug: bool):
    """A control interface for managing Kea-HA generated container images, networks, and containers."""

    # Update the app's settings with the CLI flag
    settings.debug = debug

    # Cache a reference to the app's settings within the environment and context.
    env.settings = settings

from app.cli.cmd.config import group as config_group
from app.cli.cmd.image import group as image_group
from app.cli.cmd.service import group as service_group
