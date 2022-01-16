import click
import yaml
from aiohttp import web

from apps.app import make_application


@click.group()
@click.option('--config-file', '-c', default='config.yml')
@click.pass_context
def main(ctx, config_file) -> None:
    """Manage exchnage api module."""
    with open(config_file, 'r') as ymlfile:
        settings = yaml.safe_load(ymlfile)

    ctx.obj = {
        'settings': settings,
    }


@main.command()
@click.option('--port', '-p', default='8081')
@click.option('--host', '-h', default='localhost')
@click.pass_context
def runserver(ctx, port: int, host: str) -> None:
    """Run web app on post and host.

    Example: python manage.py runserver
    Default port: 8080;
    Default host: localhost;

    """
    settings = dict(ctx.obj['settings'])

    web.run_app(make_application(settings), port=port, host=host)


if __name__ == '__main__':
    main()