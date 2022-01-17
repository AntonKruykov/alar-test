from aiohttp import web

from apps.routes.views import PointListView, RouteListView, RouteDetailView, \
    CreateRouteView


def init_routes(app: web.Application) -> None:
    """Apps routers."""
    app.add_routes([
        web.view('/points', PointListView, name='points'),
        web.view('/routes', RouteListView, name='routes'),
        web.view('/routes/create', CreateRouteView, name='route-create'),
        web.view(
            r'/routes/{item_id:\d+}',
            RouteDetailView,
            name='route-detail',
        ),
    ])
