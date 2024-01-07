from app.cli.entry import cli


@cli.group('service')
def group():
    """Manages the Kea-HA container services."""
    pass


from app.cli.service.install import install
from app.cli.service.reinstall import reinstall
from app.cli.service.restart import restart
from app.cli.service.start import start
from app.cli.service.status import status
from app.cli.service.stop import stop
from app.cli.service.uninstall import uninstall
