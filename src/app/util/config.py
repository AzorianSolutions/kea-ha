import os
import typing
import yaml
from pathlib import Path


class ConfigUtil:
    """A class for working with configuration related data and files."""

    @staticmethod
    def flatten(config: dict[str, typing.Any], prefix: str = '') -> dict[str, typing.Any]:
        result: dict[str, typing.Any] = {}

        for key, value in config.items():
            key = key.upper()
            if isinstance(value, dict):
                result.update(ConfigUtil.flatten(value, f'{prefix}{key}_'))
            else:
                result[f'{prefix}{key}'] = value

        return result


class ConfigLoader:
    """A class for loading simple configuration settings from a text file."""

    @staticmethod
    def load_file(path: Path or str) -> dict[str, typing.Any]:
        """Loads the given configuration file and returns a dictionary of key/value pairs."""
        config: dict[str, typing.Any] = {}

        if not os.path.exists(path):
            return config

        with open(path) as f:
            for line in f.read().splitlines():
                key, value = line.split('=')
                config[key.strip().lower()] = value.strip()
            f.close()

        return config

    @staticmethod
    def load_yaml(path: Path or str) -> dict[str, typing.Any]:
        """Loads the given configuration file and returns a dictionary of key/value pairs."""
        from yaml import YAMLError

        config: dict[str, typing.Any] = {}

        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            return config

        try:
            with open(path, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                f.close()
        except FileNotFoundError:
            # print(f'The given path for the configuration file does not exist: {config_path}')
            pass
        except IsADirectoryError:
            # print(f'The given path for the configuration file is not a file: {config_path}')
            pass
        except PermissionError:
            # print(f'Permission denied when trying to read the configuration file: {config_path}')
            pass
        except UnicodeDecodeError:
            # print(f'Failed to decode the configuration file: {config_path}')
            pass
        except YAMLError as e:
            # print(f'Failed to parse the configuration file "{config_path}": {e}')
            pass

        return config


class ConfigBuilder:
    """A class for building configuration files."""

    @staticmethod
    def build_env_file(config: dict) -> str:
        """Builds a .env style file from the given configuration dictionary."""
        env_file: str = ''
        env_config = ConfigUtil.flatten(config)

        for key, value in env_config.items():
            if isinstance(value, bool):
                value = str(value).lower()
            elif isinstance(value, list):
                value = ','.join(value)
            elif isinstance(value, dict):
                value = ','.join([f'{k}:{v}' for k, v in value.items()])
            elif isinstance(value, str):
                value = value.strip()
                if ' ' in value:
                    value = f'"{value}"'

            env_file += f'{key}={value}\n'

        return env_file
