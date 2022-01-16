import random
from random import randint
from typing import Callable, List

import pytest

from apps.auth.models import AuthUser
from apps.routes.models import Point, RouteItem, Route


@pytest.fixture
def point_factory(object_factory) -> Callable:
    async def factory(**kwargs):
        return await object_factory(
            Point,
            **kwargs,
        )
    return factory


@pytest.fixture
async def point(point_factory) -> Point:
    return await point_factory(
        name='Point',
        latitude=randint(0, 1000),
        longitude=randint(0, 1000),
    )


@pytest.fixture
def point_batch_factory(point_factory):
    async def factory(point_amount):
        return [
            await point_factory(
                name=f'Point {index}',
                latitude=randint(0, 1000),
                longitude=randint(0, 1000),
            ) for index in range(point_amount)
        ]
    return factory


@pytest.fixture
async def point_batch(point_batch_factory) -> List[Point]:
    return await point_batch_factory(100)


@pytest.fixture
def route_item_factory(object_factory) -> Callable:
    async def factory(**kwargs):
        return await object_factory(
            RouteItem,
            **kwargs,
        )
    return factory


@pytest.fixture
async def route_factory(
    object_factory,
    route_item_factory,
) -> Callable:
    async def factory(user: AuthUser, name: str, points: List[Point]):
        route = await object_factory(
            Route,
            user=user,
            name=name,
        )
        point_order = zip(points, range(len(points)))
        route.points = [
            await route_item_factory(
                route=route,
                point=point,
                order=order
            ) for (point, order) in list(point_order)
        ]
        return route
    return factory


@pytest.fixture
async def route(
    route_factory: Callable,
    auth_user: AuthUser,
    point_batch: List[Point],
):
    random.shuffle(point_batch)
    return await route_factory(
        auth_user,
        'Route',
        point_batch[:random.randint(2, 100)],
    )
