from aiohttp import web

from apps.report.views import RouteReportView


def init_routes(app: web.Application) -> None:
    """Apps routers."""
    app.add_routes([
        web.view('/routes', RouteReportView, name='routes'),
    ])
