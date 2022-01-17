import aiohttp

from apps.report.routers import init_routes


def make_application() -> aiohttp.web.Application:
    """Init app."""
    app = aiohttp.web.Application()
    app['verbose_name'] = 'report'
    init_routes(app)

    return app
