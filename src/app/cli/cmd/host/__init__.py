from app.cli.entry import cli


@cli.group('host')
def group():
    """Manages a Kea-HA container host."""
    pass
