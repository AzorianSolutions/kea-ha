import os
from pathlib import Path
from pydantic_settings import BaseSettings
from app.util.config import ConfigLoader

DEFAULT_CONFIG_PATH: Path = Path('defaults.yml')
base_config: dict = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)


class AppSettings(BaseSettings):
    """ The application settings class that loads setting values from the application environment. """

    _config: dict | None = None
    """ Additional configuration settings loaded automatically from the YAML file given in the config_path setting. """

    config_path: str | Path = 'config.yml'
    """ The path to the YAML file containing additional configuration settings. """

    debug: bool = False
    """ Whether debug mode is enabled. """

    env_file: str | Path | None = None
    """ The path to the environment file to load settings from. """

    env_file_encoding: str = 'UTF-8'
    """ The file encoding of the environment file to load settings from. """

    env_secrets_dir: str | Path | None = None
    """ The path to the secrets directory to load environment variable values from. """

    root_path: str | Path = Path(os.getcwd())
    """ The root path of the application which is typically the project repository root directory. """

    version: str = base_config['project']['version']
    """ The application version number """

    @property
    def config(self) -> dict:
        """ Returns the configuration data provided by the YAML file given in the config_path setting. """

        # Load the YAML configuration file if it exists and has not already been loaded
        if self._config is None:
            if DEFAULT_CONFIG_PATH.exists():
                self._config = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)

            if isinstance(self.config_path, Path | str) and Path(self.config_path).exists():
                if self._config is None:
                    self._config = ConfigLoader.load_yaml(self.config_path)
                else:
                    self._config.update(ConfigLoader.load_yaml(self.config_path))

        return self._config

    class Config:
        env_prefix = base_config['project']['environment']['prefix'] + '_'
        env_nested_delimiter = '__'
