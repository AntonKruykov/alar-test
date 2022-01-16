import pytest
from aiohttp import web


@pytest.fixture
def router_auth(app: web.Application) -> web.UrlDispatcher:
    """Fixture for auth router."""
    return app['auth'].router


@pytest.fixture
def router_routes(app: web.Application) -> web.UrlDispatcher:
    """Fixture for auth router."""
    return app['routes'].router

