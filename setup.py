import typing
from setuptools import setup

config: dict[str, typing.Any] = {}

with open('config.txt') as f:
    for line in f.read().splitlines():
        key, value = line.split('=')
        config[key.strip().lower()] = value.strip()
    f.close()

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()
    f.close()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    f.close()

setup(
    name=config['name'],
    version=config['version'],
    package_dir={'': 'src'},
    install_requires=required_packages,
    entry_points={
        'console_scripts': [
            config['cmd_name'] + ' = app.cli.entry:cli',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)
