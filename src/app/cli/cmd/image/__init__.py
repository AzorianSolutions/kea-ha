from app.cli.entry import cli


@cli.group('image')
def group():
    """Manages the Kea-HA container images."""
    pass
