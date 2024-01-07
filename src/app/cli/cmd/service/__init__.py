from app.cli.entry import cli


@cli.group('service')
def group():
    """Manages the Kea-HA container services."""
    pass


from app.cli.cmd.service.install import install
from app.cli.cmd.service.reinstall import reinstall
from app.cli.cmd.service.restart import restart
from app.cli.cmd.service.start import start
from app.cli.cmd.service.status import status
from app.cli.cmd.service.stop import stop
from app.cli.cmd.service.uninstall import uninstall
