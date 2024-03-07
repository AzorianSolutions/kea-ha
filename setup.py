import subprocess
import sys
from setuptools import setup


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def load_config() -> dict:
    import yaml
    with open('defaults.yml') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_requirements() -> list:
    with open('requirements.txt') as f:
        return f.read().splitlines()


def load_readme() -> str:
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


install('pyyaml')
config = load_config()

setup(
    name=config['app']['name'],
    version=config['app']['version'],
    package_dir={'': 'src'},
    install_requires=load_requirements(),
    entry_points={
        'console_scripts': [
            config['app']['cli']['entrypoint'] + ' = app.cli.entry:cli',
        ],
    },
    long_description=load_readme(),
    long_description_content_type='text/markdown',
)
