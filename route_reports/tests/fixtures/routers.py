import pytest
from aiohttp import web


@pytest.fixture
def router_report(app: web.Application) -> web.UrlDispatcher:
    """Fixture for report router."""
    return app['report'].router
