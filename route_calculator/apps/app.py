import asyncio
from typing import Dict, Tuple

from aiohttp import web

from apps.optimal.app import make_application as optimal_app
from helpers.jwt.middlewares import jwt_middleware


async def make_application(settings: Dict, loop=None) -> web.Application:
    """Create web app."""
    if settings is None:
        raise RuntimeError('Settings not found.')

    if loop is None:
        loop = asyncio.get_event_loop()

    app = web.Application(
        debug=settings['base']['debug'],
        middlewares=[
            jwt_middleware(
                secret_or_pub_key=settings['base']['secret'],
            ),
        ],
    )

    app['settings'] = settings

    setup_subapps(app)

    return app


def setup_subapps(app: web.Application) -> None:
    """Setup subapps."""
    sub_applications = get_subapps()

    for subapp in sub_applications:
        app.add_subapp(f'/api/{subapp["verbose_name"]}/', subapp)
        app[subapp['verbose_name']] = subapp


def get_subapps() -> Tuple:
    """Get subapps."""
    return (
        optimal_app(),
    )
