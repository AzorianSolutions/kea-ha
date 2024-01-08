import os
import subprocess
from subprocess import CompletedProcess


class Run:
    """ A callable class to run subprocess commands with environment extension. """

    @staticmethod
    def c(command: list, env: dict = None, **kwargs) -> CompletedProcess:
        if env is None:
            env = os.environ.copy()

        return subprocess.run(command, env=env, **kwargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
