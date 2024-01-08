import click
import os
from docker.errors import APIError, BuildError
from loguru import logger
from pathlib import Path
from app.cli.entry import pass_environment
from app.model.cli import Environment
from app.model.images import ImageRepo
from app.util.config import ConfigBuilder
from . import group

HLP_OPT_YES = 'Automatically answer yes to all prompts.'
HLP_OPT_NO_CACHE = 'Do not use cache when building the container image.'
HLP_OPT_STAGE = 'The stage to build from the container image.'
HLP_ARG_TAG = 'The image path, optionally including the repository URL, image name, and tag.'


@group.command('build')
@click.option('-y', '--yes', is_flag=True, default=False, help=HLP_OPT_YES)
@click.option('-nc', '--no-cache', is_flag=True, default=False, help=HLP_OPT_NO_CACHE)
@click.option('-s', '--stage', default=None, help=HLP_OPT_STAGE)
@click.argument('tag', default=None, required=False, metavar=HLP_ARG_TAG)
@pass_environment
def command(env: Environment, yes: bool, no_cache: bool, stage: str, tag: str):
    """Builds the container image for the given tag."""
    import docker

    config = env.settings.get_config

    if tag:
        repo = ImageRepo.from_tag(tag)
    else:
        meta = config('image.repository')
        repo = ImageRepo(meta['url'], meta['name'], meta['tag'])

    version: str = config('kea.version')

    if not yes:
        confirm = click.confirm('Are you sure you want to build the container image?', default=None)

        if not confirm:
            logger.warning('Aborting container image build process for lack of user confirmation or the `-y` flag.')
            return

        click.echo('What version of the Kea software would you like to build?\n')

        version_input = click.prompt('Kea Version', default=env.settings.get_config('kea.version'))

        if version_input:
            version = version_input

    logger.info(f'Building the container image...')

    env_file = Path(env.settings.get_config('app.environment.file'))

    # Save the environment file if the path is writable
    if not os.access(env_file, os.W_OK):
        logger.error(f'Failed to write the environment file: {env_file}')
        return

    # Build the environment file
    file_contents = ConfigBuilder.build_env_file(env.settings.config)

    with open(env_file, 'w') as f:
        f.write(file_contents)
        f.close()

    os.environ['DOCKER_BUILDKIT'] = '1'

    client = docker.from_env()

    build_args: dict = {
        'KHA_SHARE_PATH': config('image.paths.share'),
        'KEA_VERSION': version,
    }

    labels: dict = {}

    hosts: dict = {}

    command_args: dict = {
        'path': str(env.settings.root_path),
        'dockerfile': 'deploy/docker/Dockerfile',
        'tag': repo.repo_path,
        'nocache': no_cache,
        'target': stage,
        'buildargs': build_args,
        'labels': labels,
        'extra_hosts': hosts,
        'network_mode': 'host',
        'encoding': 'utf-8',
        'rm': True,
        'pull': True,
        'forcerm': False,
        'quiet': False,
    }

    build_success: bool = False
    build_response: str = ''

    try:
        img, logs = client.images.build(**command_args)
        build_success = True

        output: str = '\n'

        for k, v in img.labels.items():
            output += f'{k}: {v}\n'

        if env.debug:
            log_method = logger.info
        else:
            log_method = logger.debug

        log_method(f'\n{output}')

    except APIError as e:
        build_response = e.response
    except BuildError as e:
        build_response = e.msg

    if build_success:
        logger.success(f'Finished building container image!')
        return

    logger.error(f'Failed to build the container image: {build_response}')
