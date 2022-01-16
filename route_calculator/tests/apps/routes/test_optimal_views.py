import json
import random

import pytest


class TestCalcOptimalRouteView(object):

    @pytest.fixture
    def url(self, router_optimal):
        return router_optimal['optimal-route'].url_for()

    async def test_create(self, client, url, token):
        payload = {
            'name': 'New route',
            'point_a': {
                'id': 1,
                'name': 'Point A',
                'latitude': random.randint(0, 1000),
                'longitude': random.randint(0, 1000),
            },
            'point_b': {
                'id': 2,
                'name': 'Point B',
                'latitude': random.randint(0, 1000),
                'longitude': random.randint(0, 1000),
            },
            'items': [
                {
                    'point': {
                        'id': index + 3,
                        'name': f'Point {index + 3}',
                        'latitude': random.randint(0, 1000),
                        'longitude': random.randint(0, 1000),
                    },
                } for index in range(random.randint(2, 100))
            ],
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
        assert data['message'] == 'New route will be create soon.'
