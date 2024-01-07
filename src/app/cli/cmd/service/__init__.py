from app.cli.entry import cli


@cli.group('service')
def group():
    """Manages the Kea-HA container services."""
    pass
