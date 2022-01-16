import aiohttp

from apps.auth.routers import init_routes


def make_application() -> aiohttp.web.Application:
    """Init app."""
    app = aiohttp.web.Application()
    app['verbose_name'] = 'auth'
    init_routes(app)

    return app
