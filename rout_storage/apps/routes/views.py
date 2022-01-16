from aiohttp import web

from apps.routes.models import Point, Route, RouteItem
from apps.routes.serializers import PointSerializer, RouteListSerializer, \
    RouteDetailSerializer
from helpers.views import BaseListView, BaseView, BaseDetailView


class PointListView(BaseListView):

    serializer_class = PointSerializer
    query = Point.select()


class RouteListView(BaseListView):

    serializer_class = RouteListSerializer
    query = Route.select()


class RouteItemsMixin(object):

    async def get_route_items(self, route: Route):
        return await self.database.execute(
            RouteItem.select(
                RouteItem,
                Point,
            ).join(
                Point,
                on=(RouteItem.point == Point.id),
            ).where(
                RouteItem.route == route,
            ).order_by(
                RouteItem.order,
            )
        )


class RouteCreateDetailView(RouteItemsMixin, BaseDetailView):

    serializer_class = RouteDetailSerializer

    async def get_instance(self) -> Route:
        instance = await self.database.get(
            Route,
            id=self.request.match_info.get('item_id')
        )
        instance.items = await self.get_route_items(instance)
        return instance


class CreateRouteView(RouteItemsMixin, BaseView):

    serializer_class = RouteDetailSerializer

    async def post(self):

        data = await self.validate_data()
        # todo: validate if all points are exist
        instance = await self.database.create(
            Route,
            name=data['name'],
            user_id=self.request['user']['user_id']
        )

        for point in data['items']:
            await self.database.create(
                RouteItem,
                route=instance,
                point_id=point['point_id'],
                order=point['order']
            )

        instance.items = await self.get_route_items(instance)

        return web.json_response(
            self.serializer_class().dump(instance),
            status=201,
        )
