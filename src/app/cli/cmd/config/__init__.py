from app.cli.entry import cli


@cli.group('config')
def group():
    """Manages the Kea-HA configuration."""
    pass
