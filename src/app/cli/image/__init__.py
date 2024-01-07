from app.cli.entry import cli


@cli.group('image')
def group():
    """Manages the Kea-HA container images."""
    pass


from app.cli.image.build import build
from app.cli.image.pull import pull
from app.cli.image.purge import purge
from app.cli.image.push import push
