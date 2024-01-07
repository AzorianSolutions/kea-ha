import os
from pathlib import Path
from pydantic.fields import FieldInfo
from pydantic_settings import (
    EnvSettingsSource, BaseSettings, PydanticBaseSettingsSource
)
from typing import Any, Type, Tuple
from app.util.config import ConfigLoader

DEFAULT_CONFIG_PATH: Path = Path('defaults.yml')
base_config: dict = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)


class SettingsSource(EnvSettingsSource):
    def prepare_field_value(
            self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        path_fields = ['config_path', 'env_file', 'env_secrets_dir', 'root_path']

        if field_name == 'root_path' and value in ['.', './']:
            print('TEST TEST TEST')
            value = Path(os.getcwd())

        if field_name in path_fields and value is not None and not isinstance(value, Path):
            value = Path(value)

        return value


class AppSettings(BaseSettings):
    """ The application settings class that loads setting values from the application environment. """

    _config: dict | None = None
    """ Additional configuration settings loaded automatically from the YAML file given in the config_path setting. """

    _root_path: Path = Path(os.getcwd())
    """ The root path of the application which is typically the project repository root directory. """

    config_path: str | Path = 'config.yml'
    debug: bool = False
    env_file: str | Path = '.env'
    env_file_encoding: str = 'UTF-8'
    env_secrets_dir: str | Path | None = None
    version: str = base_config['project']['version']
    """ The application version number """

    @property
    def config(self) -> dict[str, Any]:
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

    @property
    def root_path(self) -> Path:
        """ Returns the root path of the application which is typically the project repository root directory. """
        return self._root_path

    class Config:
        env_prefix = base_config['project']['environment']['prefix'] + '_'
        env_nested_delimiter = '__'

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (SettingsSource(settings_cls),)
