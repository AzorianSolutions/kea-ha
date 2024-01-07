import typing
import yaml
from setuptools import setup

config: dict[str, typing.Any] = {}

with open('defaults.yml') as f:
    config.update(yaml.load(f, Loader=yaml.FullLoader))
    f.close()

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()
    f.close()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    f.close()

setup(
    name=config['project']['name'],
    version=config['project']['version'],
    package_dir={'': 'src'},
    install_requires=required_packages,
    entry_points={
        'console_scripts': [
            config['cli']['entrypoint'] + ' = app.cli.entry:cli',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)
