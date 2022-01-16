import asyncio
from typing import Dict, Tuple

from aiohttp import web

from peewee_async import Manager

from apps.auth.app import make_application as auth_app
from apps.routes.app import make_application as routes_app
from helpers.jwt.middlewares import jwt_middleware
from helpers.models import database


async def make_application(settings: Dict, loop=None) -> web.Application:
    """Create web app."""
    if settings is None:
        raise RuntimeError('Settings not found.')

    if loop is None:
        loop = asyncio.get_event_loop()

    whitelist = (
        '/api/auth/login',
    )

    app = web.Application(
        debug=settings['base']['debug'],
        middlewares=[
            jwt_middleware(
                secret_or_pub_key=settings['base']['secret'],
                whitelist=whitelist,
            ),
        ],
    )

    app['settings'] = settings
    await setup_database(app, loop)

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
        auth_app(),
        routes_app(),
    )


async def setup_database(app: web.Application, loop) -> None:
    """Setup database."""
    if 'settings' not in app:
        raise RuntimeError('Setup settings at first.')

    database.init(**app['settings']['database'])
    database.set_allow_sync(False)

    app['database'] = database
    app['objects'] = Manager(app['database'], loop=loop)
