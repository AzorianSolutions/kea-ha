from app.model.settings import AppSettings
from app.util.object import Reflective


class Environment:
    """ The application environment class that provides access to the environment settings and configuration. """

    _settings: AppSettings = None
    """ The environment settings. """

    _config: Reflective = None
    """ The environment configuration. """

    @property
    def settings(self) -> AppSettings:
        """ Returns the app's settings. """
        return self._settings

    @settings.setter
    def settings(self, value: AppSettings):
        """ Sets the app's settings. """
        self._settings = value
        if self.config is None:
            self._config = Reflective(ref=value.config)
            self._config.debug = value.debug

    @property
    def config(self) -> Reflective:
        """ Returns the environment configuration. """
        return self._config

    @property
    def c(self) -> Reflective:
        """ Returns the environment configuration. """
        return self._config

    @property
    def debug(self) -> bool:
        """ Returns whether debug mode is enabled. """
        return self._settings.debug if isinstance(self._settings, AppSettings) else False
