import click
from app.cli.entry import pass_environment
from app.model.cli import Environment
from app.util.object import Reflective
from . import group

meta_help: dict = {
    'flat': 'Flattens the JSON output to a single line.',
}

config_data: dict = {
    'app': {
        'name': 'my-app',
        'version': '0.1.0',
    },
    'list1': ['item1', 'item2', 'item3'],
    'list2': [
        {'name': 'item1', 'value': 'value1'},
        {'name': 'item2', 'value': 'value2'},
        {'name': 'item3', 'value': 'value3'},
    ],
    'image': {
        'build': {
            'dockerfile': 'Dockerfile',
            'args': {
                'APP_NAME': '$c{app/name}',
                'APP_VERSION': '$c{app/version}',
            },
        },
        'repository': {
            'url': 'cloudsmith.io',
            'name': '$c{app/name}',
            'tag': '$c{app/version}',
        },
    },
}


def log(env: Environment, message: str = None, payload: any = None, **kwargs) -> None:
    """Prints a message to the console."""

    click.echo()

    if message:
        click.echo(message)
        click.echo()

    if payload:
        click.echo('Payload:')
        click.echo(payload)
        click.echo()

    if kwargs:
        click.echo('Kwargs:')
        click.echo(str(kwargs))
        click.echo()

    click.echo()


@group.command('pg')
@click.argument('key', required=False, default=None, metavar='<KEY>')
@pass_environment
def wrapper(env: Environment, key: str = None):
    """Provides a development playground for quickly testing code."""
    return command(env, key)


def command(env: Environment, key: str = None) -> bool:
    """Provides a development playground for quickly testing code."""

    c = Reflective(config_data)
    c.debug = False
    c.parsing = True

    # log(env=env, payload=c.yaml())

    # log(env, f'Test Reference: {c("image/repository/url")}')
    #
    # c('image/repository/url')('docker.io')
    #
    # log(env, f'Test Reference: {c.image.repository.url}')
    #
    # c['image.build.dockerfile'] = 'Dockerfile2'
    #
    # log(env, f'Image Reference: {c.image}')
    #
    # log(env, f'Image Reference: {c.image}')

    log(env, f'List 1 Reference: {c.list1}')

    # c.update('list1', ['item4', 'item5', 'item6'])
    c['list1'] = ['item4', 'item5', 'item6']

    log(env, f'List 1 Reference: {c.list1}')

    # c.list1 = ['item5', 'item6', 'item7']
    c.list1[1] = 'test item'

    c.list1 += ['item7', 'item8', {'test1': 'value1', 'test2': 'value2'}]

    log(env, f'List 1 Reference: {c.list1}')

    c.list1[5]['test2'] = 'value3'

    log(env, f'List 1 Reference: {c.list1}')

    # Property Update Testing

    # c.app.name = 'app2'
    # log(env, f'app2: {c.app}')
    #
    # c.app.update('name', 'app3')
    # log(env, f'app3: {c.app}')
    # log(env, f'app3: {c.app.name}')
    #
    # c.update('app.name', 'app5')
    # log(env, f'app5: {c.app}')

    # Property Access Testing

    # log(env, f'image.build.args: {c.image.build.args}')
    #
    # config_data['image']['build']['args']['test1'] = '$c{app/name}'
    #
    # log(env, f'image.build.args: {c.image.build.args}')
    # log(env, f'image.build.args: {c.image.build("args")}')
    # log(env, f'image.build.args: {c.image("build.args")}')
    # log(env, f'image.build.args: {c("image.build.args")}')
    #
    # log(env, f'image.build.args: {c["image"]["build"]["args"]}')
    # log(env, f'image.build.args: {c["image.build.args"]}')
    # log(env, f'image.build.args: {c["image/build/args"]}')
    # log(env, f'image.build.args: {c["image__build__args"]}')

    return True

    if key is None:
        click.echo(env.config)
        return True

    env.c.parsing = True

    log(env, f'Test: {env.c.image.build.dockerfile}')
    env.c.image.build.dockerfile = '$c{app/version}'
    log(env, f'Test: {env.c.image.build.dockerfile}')

    original = env.c.image.repository.copy()
    log(env, f'image.repository: {env.c.image.repository.json()}')
    env.c.image.repository = {'url': 'cloudsmith.io', 'name': '$c{app/name}', 'tag': '$c{app/version}'}
    log(env, f'image.repository: {env.c.image.repository}')
    # env.c.image.repository = original
    # log(env, f'image.repository: {env.c.image.repository}')

    # env.c.parsing = False

    # log(env, f'image.repository: {env.c.image.repository}')

    # env.c.parsing = True

    # log(env, f'image.repository: {env.c.image.repository}')

    log(env, f'image.build.args: {env.c.image.build.args}')
    log(env, f'image.build.args: {env.c.image.build("args")}')
    log(env, f'image.build.args: {env.c.image("build.args")}')
    log(env, f'image.build.args: {env.c["image"]["build"]["args"]}')
    log(env, f'image.build.args: {env.c["image.build.args"]}')
    log(env, f'image.build.args: {env.c["image/build/args"]}')
    log(env, f'image.build.args: {env.c["image__build__args"]}')


    return True
