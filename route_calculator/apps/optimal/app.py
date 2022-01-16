import aiohttp
from aiojobs.aiohttp import setup as aiojob_setup

from apps.optimal.routers import init_routes


def make_application() -> aiohttp.web.Application:
    """Init app."""
    app = aiohttp.web.Application()
    app['verbose_name'] = 'optimal'
    aiojob_setup(app)
    init_routes(app)

    return app
