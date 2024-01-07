import click
import sys
from app.config import AppSettings


class Environment:
    _settings: AppSettings = None

    @property
    def debug(self) -> bool:
        """ Returns whether debug mode is enabled. """
        return self._settings.debug if isinstance(self._settings, AppSettings) else False

    @property
    def settings(self) -> AppSettings:
        """ Returns the app's settings. """
        return self._settings

    @settings.setter
    def settings(self, value: AppSettings):
        """ Sets the app's settings. """
        self._settings = value

    @staticmethod
    def log(msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.debug:
            self.log(msg, *args)
