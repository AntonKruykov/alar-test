import json
import random

from aiohttp import web, ClientSession
from aiojobs.aiohttp import spawn

from apps.optimal.serializers import (
    CreateOptimalRouteSerializer,
    RouteSerializer
)
from helpers.views import BaseView


class CalcOptimalRouteView(BaseView):

    serializer_class = CreateOptimalRouteSerializer

    async def post(self):

        data = await self.validate_data()

        await spawn(
            self.request,
            self.calc_optimal_route(data),
        )

        return web.json_response(
            {'message': 'New route will be create soon.'},
            status=201,
        )

    async def calc_optimal_route(self, data):

        points = [
            point['point'] for point in data['items']
        ]
        random.shuffle(points)
        optimal_route = [data['point_a'], *points, data['point_b']]
        route_order = zip(optimal_route, range(len(optimal_route)))
        route = {
            'name': data['name'],
            'items': [
                {
                    'point_id': point['id'],
                    'order': order
                } for (point, order) in list(route_order)
            ]
        }
        payload = RouteSerializer().dump(route)

        async with ClientSession() as client:
            await client.post(
                self.settings['create_route_url'],
                data=json.dumps(payload),
                headers={
                    'Authorization': self.request.headers['Authorization'],
                },
            )
