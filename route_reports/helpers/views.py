import json
from typing import Dict

from aiohttp import web
from marshmallow import ValidationError
from peewee import Query
from peewee_async import PooledPostgresqlDatabase


class BaseView(web.View):

    @property
    def serializer_class(self):
        raise NotImplementedError

    @property
    def database(self) -> PooledPostgresqlDatabase:
        """Database property."""
        return self.request.config_dict['objects']

    async def validate_data(self, partial=False) -> Dict:
        """Validate request data."""
        try:
            request_data: Dict = await self.request.json()
        except json.decoder.JSONDecodeError:
            raise web.HTTPBadRequest(
                text=json.dumps({'error': ['Bad request.']}),
                content_type='application/json',
            )

        try:
            return self.serializer_class().load(
                request_data,
                partial=partial,
            )
        except ValidationError as error:

            raise web.HTTPBadRequest(
                text=json.dumps({'error': error.messages}),
                content_type='application/json',
            )


class BaseListView(BaseView):

    @property
    def serializer_class(self):
        raise NotImplementedError

    @property
    def query(self) -> Query:
        raise NotImplementedError

    async def get(self):
        limit = self.request.rel_url.query.get('limit', 100)
        offset = self.request.rel_url.query.get('offset', 0)

        count = await self.database.count(self.query.clone())

        points = await self.database.execute(
            self.query.limit(limit).offset(offset),
        )

        results = self.serializer_class(many=True).dump(points)

        return web.json_response(
            {
                'count': count,
                'offset': offset,
                'limit': limit,
                'results': results,
            }
        )
