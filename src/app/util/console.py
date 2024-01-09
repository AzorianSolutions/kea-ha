import os
import subprocess
from loguru import logger
from pathlib import Path
from subprocess import CompletedProcess
from app.model.cli import Environment


class Run:
    """ A callable class to run subprocess commands with environment definition. """

    @staticmethod
    def c(command: list, env: Environment, process_env: dict = None, **kwargs) -> CompletedProcess:
        """ Runs the given command with the given environment, copies the current environment if None given. """

        # Copy the current environment if none given
        if env is None:
            env = os.environ.copy()

        if env.debug:
            from loguru import logger
            logger.debug(f'Running Command: {command}')

        return subprocess.run(command, env=process_env, **kwargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def compose(command: list, env: Environment, **kwargs) -> CompletedProcess | bool:

        compose_file = Path(env.settings.c('service/paths/compose/file'))
        env_file = Path(env.settings.c('service/paths/compose/env'))

        if not compose_file.exists():
            logger.error(f'Failed to find the compose file: {compose_file}')
            return False

        if not env_file.exists():
            logger.error(f'Failed to find the environment file: {env_file}')
            return False

        compose_cmd: list = [
            f'docker',
            'compose',
            '--project-directory',
            f'{env.settings.root_path}',
            '--env-file',
            f'{env_file}',
            '-f',
            f'{compose_file}'
        ]

        compose_cmd.extend(command)

        return Run.c(compose_cmd, env, None, **kwargs)
