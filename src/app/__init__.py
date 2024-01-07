import os
import typing
from pathlib import Path
from app.model.settings import AppSettings
from app.util.config import ConfigLoader

ROOT_PATH: Path = Path(os.getcwd())
""" The root path of the application which is typically the project repository root directory."""

DEFAULT_CONFIG_PATH: Path = ROOT_PATH / 'defaults.yml'
""" The file containing the default YAML configuration to use when an environment specific file is missing. """

SRC_PATH: Path = ROOT_PATH / 'src'
""" The source path of the application which is typically the src directory within the ROOT_PATH. """

DEFAULT_ENV_PATH: Path = ROOT_PATH / '.env'
""" The default path to the environment file to load settings from. """

DEFAULT_ENV_FILE_ENCODING: str = 'UTF-8'
""" The default file encoding of the environment file to load settings from. """

DEFAULT_SECRETS_PATH: Path | None = None
""" The default path to the secrets directory to load environment variable values from. """

base_config: dict[str, typing.Any] = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)


def load_settings(env_file_path: str | Path | None = None, env_file_encoding: str | None = None,
                  secrets_path: str | Path | None = None) -> AppSettings:
    """ Loads an AppSettings instance based on the given environment file and secrets directory. """

    # Extract the default environment file path from the environment if defined, otherwise use the default path
    if env_file_path is None:
        env_file_path = os.getenv(f'{base_config["project"]["environment"]["prefix"]}_ENV_FILE', DEFAULT_ENV_PATH)

    # Extract the default environment file encoding from the environment if defined, otherwise use the default value
    if env_file_encoding is None:
        env_file_encoding = os.getenv(f'{base_config["project"]["environment"]["prefix"]}_ENV_FILE_ENCODING', DEFAULT_ENV_FILE_ENCODING)

    # Extract the default secrets directory path from the environment if defined, otherwise use the default path
    if secrets_path is None:
        secrets_path = os.getenv(f'{base_config["project"]["environment"]["prefix"]}_ENV_SECRETS_DIR', DEFAULT_SECRETS_PATH)

    if env_file_path is not None and not isinstance(env_file_path, Path):
        env_file_path = Path(env_file_path)

    if secrets_path is not None and not isinstance(secrets_path, Path):
        secrets_path = Path(secrets_path)

    params: dict = {
        '_env_file': env_file_path,
        '_env_file_encoding': env_file_encoding,
    }

    os.putenv(f'{base_config["project"]["environment"]["prefix"]}_ENV_FILE', str(env_file_path))
    os.putenv(f'{base_config["project"]["environment"]["prefix"]}_ENV_FILE_ENCODING', env_file_encoding)

    if secrets_path is not None:
        valid: bool = True

        if not secrets_path.exists():
            valid = False
            print(f'The given path for the "--secrets-dir" option does not exist: {secrets_path}')
        elif not secrets_path.is_dir():
            valid = False
            print(f'The given path for the "--secrets-dir" option is not a directory: {secrets_path}')

        if valid:
            params['_secrets_dir'] = secrets_path
            os.putenv(f'{base_config["project"]["environment"]["prefix"]}_ENV_SECRETS_DIR', str(secrets_path))

    # Load base app configuration settings from the given environment file and the local environment
    app_settings = AppSettings(**params)

    return app_settings


settings: AppSettings = load_settings()
