
import psycopg2

import pytest
from aiohttp import web
from peewee_async import PooledPostgresqlDatabase
from peewee_moves import DatabaseManager

from apps.report.models import RouteReport

MODELS = [
    RouteReport,
]


@pytest.fixture(autouse=True, scope='session')
def setup_database(settings) -> None:
    """Init test database before testings."""
    connection_params = settings['database'].copy()
    basename = connection_params['database']
    connection_params['database'] = settings['original_database']
    conn = psycopg2.connect(
        **connection_params,
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        'DROP DATABASE IF EXISTS {0}'.format(basename),
    )
    cur.execute(
        'CREATE DATABASE {0}'.format(basename),
    )

    manager = DatabaseManager(
        PooledPostgresqlDatabase(
            **settings['database'],
        ),
    )
    manager.upgrade()


@pytest.fixture(autouse=True)
async def flush_test_tables(db):
    """Flush all tables after every test passed."""
    yield
    for model in reversed(MODELS):
        await db.execute(model.delete())


@pytest.fixture
async def db(app: web.Application, settings):
    """Get database instance."""
    return app['objects']
