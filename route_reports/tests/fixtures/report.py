import random

import pytest

from apps.report.models import RouteReport


@pytest.fixture
async def report_record(object_factory):
    return await object_factory(
        RouteReport,
        user_id=1,
        username='test@test.te',
        route_count=random.randint(1, 100),
        route_length=random.randint(50, 1000),
    )
