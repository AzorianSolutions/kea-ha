import click
from loguru import logger
from app.cli.entry import pass_environment, confirm_option
from app.model.cli import Environment
from app.model.images import ImageRepo
from . import group


@group.command('rm')
@confirm_option
@click.option('-t', '--tag', default=None, help='The tag to purge from the container image.')
@pass_environment
def wrapper(env: Environment, yes: bool, tag: str):
    """Purges the given container image or uses the default."""
    command(env, yes, tag)


def command(env: Environment, yes: bool, tag: str) -> bool:
    """Purges the given container image or uses the default."""
    import docker
    from docker.errors import APIError, ImageNotFound

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

    if not yes:
        confirm = click.confirm(f'Are you sure you want to purge the container image {repo.repo_path}?', default=None)

        if not confirm:
            logger.warning('Aborting container image purge process for lack of user confirmation or the `-y` flag.')
            return False

    logger.info(f'Purging container image {repo.repo_path}...')

    client = docker.from_env()

    try:
        client.images.remove(repo.repo_path)
    except ImageNotFound:
        logger.warning(f'Container image {repo.repo_path} not found.')
    except APIError as e:
        logger.error(f'Failed to purge container image {repo.repo_path} due to an API error: {e}')
    except Exception as e:
        logger.error(f'Failed to purge container image {repo.repo_path} due to an error: {e}')
    else:
        logger.success(f'Container image {repo.repo_path} purged.')

    return True
