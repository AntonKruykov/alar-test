import pytest
from aiohttp import web


@pytest.fixture
def router_optimal(app: web.Application) -> web.UrlDispatcher:
    """Fixture for optimal router."""
    return app['optimal'].router
