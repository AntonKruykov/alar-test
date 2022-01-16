import uuid

import click
import yaml
from aiohttp import web
from peewee_async import PooledPostgresqlDatabase
from peewee_moves import DatabaseManager

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
@click.option('--port', '-p', default='8082')
@click.option('--host', '-h', default='localhost')
@click.pass_context
def runserver(ctx, port: int, host: str) -> None:
    """Run web app on post and host.

    Example: python manage.py runserver
    Default port: 8082;
    Default host: localhost;

    """
    settings = dict(ctx.obj['settings'])

    web.run_app(make_application(settings), port=port, host=host)


@main.command()
@click.option('--model', '-m', default=None)
@click.pass_context
def makemigration(ctx, model) -> None:
    """Generate empty migration method.

    Example: python manage.py makemigration
    See path: /project_dir/migrations.

    """
    manager = DatabaseManager(
        PooledPostgresqlDatabase(
            **ctx.obj['settings']['database'],
        ),
    )

    if model:
        manager.create(model)
    else:
        manager.revision(str(uuid.uuid4()).replace('-', '_'))


@main.command()
@click.pass_context
def migrate(ctx) -> None:
    """Apply not applied migrations.

    Example: python manage.py migrate
    See path: /project_dir/migrations.

    """
    manager = DatabaseManager(
        PooledPostgresqlDatabase(
            **ctx.obj['settings']['database'],
        ),
    )

    manager.upgrade()


@main.command()
@click.option('--migration-name', '-m', required=True)
@click.pass_context
def rollback(ctx, migration_name: str) -> None:
    """Rollback migration by name of migration.

    Example: python manage.py rollback xxxx_xxxx_xxxx_xxxx_xxxx_xxxxxxxx
    See path: /project_dir/migrations.

    """
    manager = DatabaseManager(
        PooledPostgresqlDatabase(
            **ctx.obj['settings']['database'],
        ),
    )

    manager.downgrade(migration_name)


if __name__ == '__main__':
    main()