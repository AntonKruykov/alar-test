from aiohttp import web

from apps.auth.views import LoginView


def init_routes(app: web.Application) -> None:
    """Apps routers."""
    app.add_routes([
        web.view('/login', LoginView, name='login'),
    ])
