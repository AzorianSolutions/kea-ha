import click
import os
import typing
from app.cli.core import Environment
from app.config import ConfigLoader, settings

config_path: str = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.txt'))
config: dict[str, typing.Any] = ConfigLoader.load_file(config_path)
pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group()
@click.version_option(config['version'], '-V', '--version', message='%(version)s')
@click.option('-d', '--debug', default=settings.debug, is_flag=True, help='Enables debug mode.')
@pass_environment
def cli(env: Environment, debug: bool):
    """A control interface for managing Kea-HA generated container images, networks, and containers."""

    # Update the app's settings with the CLI flag
    settings.debug = debug

    # Cache a reference to the app's settings within the environment and context.
    env.settings = settings


from app.cli.config import group as config_group
from app.cli.image import group as image_group
from app.cli.service import group as service_group
