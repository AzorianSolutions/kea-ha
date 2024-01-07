import os
import typing
import yaml
from pathlib import Path


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
