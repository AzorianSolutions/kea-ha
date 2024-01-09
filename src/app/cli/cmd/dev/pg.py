import click
from app.cli.entry import pass_environment
from app.model.cli import Environment
from . import group

meta_help: dict = {
    'flat': 'Flattens the JSON output to a single line.',
}


@group.command('pg')
@click.argument('key', required=False, default=None, metavar='<KEY>')
@pass_environment
def wrapper(env: Environment, key: str = None):
    """Provides a development playground for quickly testing code."""
    return command(env, key)


def command(env: Environment, key: str = None) -> bool:
    """Provides a development playground for quickly testing code."""

    if key is None:
        click.echo(env.config)
        return True

    click.echo(getattr(env.config, key))

    return True
