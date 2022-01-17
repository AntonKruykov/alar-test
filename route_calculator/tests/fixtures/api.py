import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from apps.app import make_application


@pytest.fixture
async def app(settings, loop) -> web.Application:
    """Fixture for application."""
    return await make_application(settings, loop)


@pytest.fixture
def client_factory(aiohttp_client):
    """Factory for create client."""
    async def create(app):
        return await aiohttp_client(app)
    return create


@pytest.fixture
async def client(client_factory, app: web.Application) -> TestClient:
    """Get test client."""
    return await client_factory(app)
