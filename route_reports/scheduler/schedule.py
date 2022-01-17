import asyncio
from datetime import datetime
from typing import List

from aiohttp import ClientSession
from peewee import DoesNotExist

from apps.report.models import RouteReport, ReportUpdate
from helpers.jwt.handler import JWTHandler
from scheduler.manager import scheduler

REPORT_UPDATE = 1


async def get_data(url, token, start_id: int):

    async with ClientSession() as client:
        resp = await client.get(
            url + f'?id__gt={start_id}',
            headers={
                'Authorization': f'Bearer {token}',
            },
        )
        return await resp.json()


async def get_or_create_report_record(user_id: str, username) -> RouteReport:

    try:
        return await scheduler.database.get(
            RouteReport,
            user_id=user_id,
        )
    except DoesNotExist:
        return await scheduler.database.create(
            RouteReport,
            user_id=user_id,
            username=username,
        )


async def get_last_id():

    update_record = await scheduler.database.get(
        ReportUpdate,
        report=REPORT_UPDATE,
    )
    return update_record.last_id


async def set_last_id(last_id):

    await scheduler.database.execute(
        ReportUpdate.update(
            last_id=last_id,
        ).where(
            ReportUpdate.report == REPORT_UPDATE,
        )
    )


async def save_results(results: List):

    for result in results:
        route_report = await get_or_create_report_record(
            result['user_id'],
            result['username'],
        )
        await scheduler.database.execute(
            RouteReport.update(
                route_count=RouteReport.route_count + 1,
                route_length=RouteReport.route_length + len(result['items']),
            ).where(
                RouteReport.user_id == route_report.user_id,
            )
        )
    await set_last_id(results[-1]['id'])


async def download_report_data():
    """Download data for report."""

    token = generate_jwt()
    url = scheduler.settings.get('report_data_url')
    prev_count = 100
    while prev_count:
        start_id = await get_last_id()
        data = await get_data(url, token, start_id)
        prev_count = data['count']
        if prev_count:
            await save_results(data['results'])


def generate_jwt():
    class FakeRequest(object):
        config_dict = {
            'settings': scheduler.settings,
        }

    payload = {
        'user_id': 1,
    }
    jwt_handler = JWTHandler(FakeRequest(), payload)
    access_payload = jwt_handler.generate_payload()
    return jwt_handler.encode_jwt(access_payload)


SCHEDULED_TASKS = (
    {'func': download_report_data, 'trigger': 'interval', **{'minutes': 1}},
)
