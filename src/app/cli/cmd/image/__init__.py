from app.cli.entry import cli


@cli.group('image')
def group():
    """Manages the Kea-HA container images."""
    pass


from app.cli.cmd.image.build import build
from app.cli.cmd.image.pull import pull
from app.cli.cmd.image.purge import purge
from app.cli.cmd.image.push import push
