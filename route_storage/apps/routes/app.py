import aiohttp

from apps.routes.routers import init_routes


def make_application() -> aiohttp.web.Application:
    """Init app."""
    app = aiohttp.web.Application()
    app['verbose_name'] = 'routes'
    init_routes(app)

    return app
