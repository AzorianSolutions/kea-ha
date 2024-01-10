import click
from app.cli.entry import cli


def service_argument(function):
    """ A decorator that adds a service argument to the command. """
    meta_help = 'The service to operate on.'
    # function = click.argument('service', default='', metavar='<service>', help=meta_help)(function)
    function = click.argument('service', default='', metavar='<service>')(function)
    return function


@cli.group('service')
def group():
    """Manages the Kea-HA container services."""
    pass
