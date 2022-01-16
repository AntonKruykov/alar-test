from aiohttp import web

from apps.optimal.views import CalcOptimalRouteView


def init_routes(app: web.Application) -> None:
    """Apps routers."""
    app.add_routes([
        web.view('/optimal', CalcOptimalRouteView, name='optimal-route'),
    ])
