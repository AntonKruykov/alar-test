import json

import pytest

from apps.routes.models import Point, Route


class TestPointListView(object):

    @pytest.fixture
    def url(self, router_routes):
        return router_routes['points'].url_for()

    async def test_point_list(self, client, url, token, point: Point):
        resp = await client.get(
            url,
            headers={
                'Authorization': 'Bearer {0}'.format(token),
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data['count'] == 1
        assert data['limit'] == 100
        assert data['results'][0]['id'] == point.id
        assert data['results'][0]['name'] == point.name
        assert data['results'][0]['latitude'] == point.latitude
        assert data['results'][0]['longitude'] == point.longitude


class TestRouteListView(object):

    @pytest.fixture
    def url(self, router_routes):
        return router_routes['routes'].url_for()

    async def test_list(self, client, url, token, route: Route, dumps):
        resp = await client.get(
            url,
            headers={
                'Authorization': 'Bearer {0}'.format(token),
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data['count'] == 1
        assert data['limit'] == 100
        assert data['results'][0]['id'] == route.id
        assert data['results'][0]['name'] == route.name
        assert data['results'][0]['user_id'] == route.user_id


class TestRouteDetailView(object):

    @pytest.fixture
    def url(self, router_routes):
        def create(item_id):
            return router_routes['route-detail'].url_for(item_id=str(item_id))
        return create

    async def test_retrieve(self, client, url, token, route: Route):
        resp = await client.get(
            url(route.id),
            headers={
                'Authorization': 'Bearer {0}'.format(token),
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data['id'] == route.id
        assert data['name'] == route.name
        assert len(data['items']) == len(route.points)
        assert data['items'][0]['point']['name'] == route.points[0].point.name


class TestCreateRouteView(object):

    @pytest.fixture
    def url(self, router_routes):
        return router_routes['route-create'].url_for()

    async def test_create(self, client, url, token, point_batch, dumps):
        point_amount = 5
        payload = {
            'name': 'New route',
            'items': [
                {
                    'point_id': point_batch[index].id,
                    'order': index,
                } for index in range(point_amount)
            ]

        }
        resp = await client.post(
            url,
            headers={
                'Authorization': 'Bearer {0}'.format(token),
            },
            data=json.dumps(payload),
        )
        assert resp.status == 201
        data = await resp.json()
        assert data['name'] == payload['name']
        assert len(data['items']) == len(payload['items'])
        assert data['items'][0]['point']['name'] == point_batch[0].name
