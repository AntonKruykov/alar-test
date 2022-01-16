import asyncio
import json
import os
from typing import Dict

import pytest
import yaml

from aiohttp import ClientResponse


@pytest.fixture
def dumps():
    async def dumps_func(resp: ClientResponse):
        """Print response body human readable."""
        print()  # noqa: T001
        if resp.content:
            print(json.dumps(await resp.json(), indent=4))  # noqa: T001
    return dumps_func


@pytest.fixture(scope='session')
def loop():
    """Use asyncio loop by default."""
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True, scope='session')
def work_dir(pytestconfig) -> None:
    """Set project rootdir as work dir for tests."""
    os.chdir(pytestconfig.rootdir)


@pytest.fixture(autouse=True, scope='session')
def settings(work_dir) -> Dict:
    """Fixture for project settings."""
    with open('config.yml', 'r') as ymlfile:
        settings = yaml.safe_load(ymlfile)
    settings['original_database'] = settings['database']['database']
    test_database = '{0}_test'.format(settings['database']['database'])
    settings['database']['database'] = test_database
    return settings


@pytest.fixture
def object_factory(db):
    """Factory for create any model object."""
    async def create(model, **kwargs):
        return await db.create(model, **kwargs)
    return create
