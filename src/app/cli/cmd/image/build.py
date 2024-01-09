import click
import os
from docker.errors import APIError, BuildError
from loguru import logger
from pathlib import Path
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.model.images import ImageRepo
from app.util.config import ConfigBuilder
from . import group

HLP_OPT_YES = 'Automatically answer yes to all prompts.'
HLP_OPT_NO_CACHE = 'Do not use cache when building the container image.'
HLP_OPT_STAGE = 'The stage to build from the container image.'
HLP_ARG_TAG = 'The image path, optionally including the repository URL, image name, and tag.'


@group.command('build')
@confirm_option
@click.option('-nc', '--no-cache', is_flag=True, default=False, help=HLP_OPT_NO_CACHE)
@click.option('-s', '--stage', default=None, help=HLP_OPT_STAGE)
@click.argument('tag', default=None, required=False, metavar='<tag>')
@pass_environment
def wrapper(env: Environment, yes: bool, no_cache: bool, stage: str, tag: str):
    """Builds the container image for the given tag."""
    command(env, yes, no_cache, stage, tag)


def command(env: Environment, yes: bool, no_cache: bool, stage: str, tag: str) -> bool:
    """Builds the container image for the given tag."""
    import docker

    if tag:
        repo = ImageRepo.from_tag(tag)
        if repo.repo_url == "":
            repo.repo_url = env.settings.c('image/repository/url')
        if repo.repo_name == "":
            repo.repo_name = env.settings.c('image/repository/name')
        if repo.repo_tag == "":
            repo.repo_tag = env.settings.c('image/repository/tag')
    else:
        meta = env.settings.c('image/repository')
        repo = ImageRepo(meta['url'], meta['name'], meta['tag'])

    version: str = env.settings.c('kea/version')

    if not yes:
        confirm = click.confirm('Are you sure you want to build the container image?', default=None)

        if not confirm:
            logger.warning('Aborting container image build process for lack of user confirmation or the `-y` flag.')
            return False

        click.echo('What version of the Kea software would you like to build?\n')

        version_input = click.prompt('Kea Version', default=env.settings.c('kea/version'))

        if version_input and version_input != version:
            version = version_input

            # Save the version change back to the configuration
            env.settings.u('kea/version', version)
            env.settings.save()

    dockerfile_tpl_path = env.settings.c(f'templates/docker/dockerfile')

    # Render the Dockerfile template
    try:
        template = ConfigBuilder.build_tpl(dockerfile_tpl_path, env.settings.config)
    except FileNotFoundError as e:
        logger.error(f'Failed to find the Dockerfile template: {dockerfile_tpl_path}')
        return False

    dockerfile = Path(env.settings.c('image/build/dockerfile'))

    if not dockerfile.parent.exists():
        if not os.access(dockerfile.parent, os.W_OK):
            logger.error(f'No write permission to Dockerfile path: {dockerfile.parent}')
            return False

        logger.debug(f'Creating the Dockerfile path: {dockerfile.parent}')
        dockerfile.parent.mkdir(parents=True)

    with open(dockerfile, 'w') as f:
        f.write(template)
        f.close()

    logger.info(f'Saved the image Dockerfile: {dockerfile}')

    source_docker_ignore = env.settings.root_path / '.dockerignore'

    if not source_docker_ignore.exists():
        logger.error(f'No docker ignore file found at: {source_docker_ignore}')
        return False

    kha_root = Path(env.settings.c('service/paths/kha/root'))

    target_docker_ignore = kha_root / '.dockerignore'

    if not target_docker_ignore.parent.exists():
        if not os.access(target_docker_ignore.parent, os.W_OK):
            logger.error(f'No write permission to docker ignore path: {target_docker_ignore.parent}')
            return False

        logger.debug(f'Creating the docker ignore path: {target_docker_ignore.parent}')
        target_docker_ignore.parent.mkdir(parents=True)

    with open(source_docker_ignore, 'r') as f:
        ignore_contents = f.read()
        f.close()

    with open(target_docker_ignore, 'w') as f:
        f.write(ignore_contents)
        f.close()

    logger.info(f'Created Docker ignore file: {target_docker_ignore}')

    # Temporary until entrypoint bash script goes away
    entrypoint_tpl_path = env.settings.root_path / 'deploy' / 'docker' / 'entrypoint.sh'

    with open(kha_root / 'entrypoint.sh', 'w') as f:
        f.write(entrypoint_tpl_path.read_text())
        f.close()

    logger.info(f'Building the container image...')

    os.environ['DOCKER_BUILDKIT'] = '1'

    client = docker.from_env()

    # Additional build arguments passed to the container image
    build_args: dict = {}

    # Attempt to load additional build arguments from the configuration
    if isinstance(config_build_args := env.settings.c('image/build/args'), dict):
        build_args.update(config_build_args)

    # Additional labels added to the container image
    labels: dict = {}

    # Attempt to load additional image labels from the configuration
    if isinstance(config_labels := env.settings.c('image/labels'), dict):
        labels.update(config_labels)

    # Additional host entries added to the container's `/etc/hosts` file
    hosts: dict = {}

    # Attempt to load additional host entries from the configuration
    if isinstance(config_hosts := env.settings.c('image/hosts'), dict):
        hosts.update(config_hosts)

    dockerfile: Path = Path(env.settings.c('image/build/dockerfile'))
    build_context: Path = dockerfile.parent

    command_args: dict = {
        'path': str(build_context),
        'dockerfile': dockerfile.name,
        'tag': repo.repo_path,
        'nocache': no_cache,
        'labels': labels,
        'extra_hosts': hosts,
        'buildargs': build_args,
        'network_mode': 'host',
        'encoding': 'utf-8',
        'rm': True,
        'pull': True,
        'forcerm': False,
        'quiet': False,
    }

    if stage:
        command_args['target'] = stage

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

    if not build_success:
        logger.error(f'Failed to build the container image: {build_response}')
        return False

    logger.success(f'Finished building container image!')
    return True
