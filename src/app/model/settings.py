import os
import re
from pathlib import Path
from pydantic_settings import BaseSettings
from app.util.config import ConfigLoader, ConfigBuilder

DEFAULT_CONFIG_PATH: Path = Path('defaults.yml')
base_config: dict = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)

variable_pattern = re.compile(r'\${([A-Z]+[A-Z0-9_]*)}', re.IGNORECASE)


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

    version: str = base_config['app']['version']
    """ The application version number """

    @property
    def config(self) -> dict:
        """ Returns the configuration data provided by the YAML file given in the config_path setting. """

        # Load the YAML configuration file if it exists and has not already been loaded
        if self._config is None:
            if DEFAULT_CONFIG_PATH.exists():
                self._config = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)

            if isinstance(self.config_path, Path | str) and Path(self.config_path).exists():
                user_config = ConfigLoader.load_yaml(self.config_path)

                if user_config is None:
                    return self._config

                if self._config is None:
                    self._config = user_config
                else:
                    self._config.update(user_config)

        return self._config

    def c(self, key: str, default: any = None, parse: bool = True) -> any:
        """ Returns the configuration value for the given key, or the given default if not found. """
        from functools import reduce
        try:
            result = reduce(lambda c, k: c[k] if not k.isnumeric() else c[int(k)], key.split('__'), self.config)
        except (KeyError, TypeError):
            result = default
        if parse:
            result = self.parse(result)
        return result

    def u(self, key: str, value: any) -> None:
        """ Updates the configuration value for the given key. """

        ref = self.config

        for k in key.split('__')[:-1]:
            ref = ref[k if not k.isnumeric() else int(k)]

        ref[key.split('__')[-1]] = value

    def save(self, path: str | Path = None) -> None:
        """ Saves the current configuration to the given path, or the default if None given. """

        if path is None:
            path = self.config_path

        ConfigBuilder.save_yaml(path, self.config)

    def parse(self, value: any, default: any = None) -> any:
        """ Parses the given value for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = value.copy() if isinstance(value, dict | list) else value

        if isinstance(result, str):
            result = self.parse_string(result, default)

        elif isinstance(result, list):
            result = self.parse_list(result, default)

        elif isinstance(result, dict):
            result = self.parse_dict(result, default)

        return result

    def parse_string(self, value: str, default: any = None) -> str:
        """ Parses the given string for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        match = variable_pattern.search(value)

        if match and len(match.groups()):
            key: str = match.group(1).lower()
            config_value = self.c(key, default, False)
            value = value.replace(match.group(0), config_value)

        return value

    def parse_list(self, value: list, default: any = None) -> list:
        """ Parses the given list for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = []

        for item in value:
            result.append(self.parse(item, default))

        return result

    def parse_dict(self, value: dict, default: any = None) -> dict:
        """ Parses the given dictionary for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = {}

        for k, v in value.items():
            result[k] = self.parse(v, default)

        return result

    class Config:
        env_prefix = base_config['app']['environment']['prefix'] + '_'
        env_nested_delimiter = '__'
