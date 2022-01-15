import pytest
from aiohttp import web


@pytest.fixture
def router_auth(app: web.Application) -> web.UrlDispatcher:
    """Fixture for auth router."""
    return app['auth'].router
