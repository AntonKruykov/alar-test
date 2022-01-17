import json
from typing import Dict, List

from aiohttp import web
from marshmallow import ValidationError
from peewee import Query
from peewee_async import PooledPostgresqlDatabase

from helpers.models import BaseModel


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

    async def get_query(self) -> Query:
        return self.query

    async def execute_list_query(self, query) -> List:
        """Execute query for retrieve a list or objects.

        For example you can override this method for use prefetch()
        """
        return await self.database.execute(query)

    async def get(self):
        limit = self.request.rel_url.query.get('limit', 100)
        offset = self.request.rel_url.query.get('offset', 0)

        query = await self.get_query()

        count = await self.database.count(query.clone())

        query = query.limit(limit).offset(offset)
        items = await self.execute_list_query(query)

        results = self.serializer_class(many=True).dump(items)

        return web.json_response(
            {
                'count': count,
                'offset': offset,
                'limit': limit,
                'results': results,
            }
        )


class BaseDetailView(BaseView):

    @property
    def serializer_class(self):
        raise NotImplementedError

    @property
    def get_instance(self):
        raise NotImplementedError

    async def get(self):

        try:
            instance = await self.get_instance()
        except BaseModel.DoesNotExist:
            raise web.HTTPNotFound(
                text=json.dumps({
                    'error': ['Object not found.'],
                }),
                content_type='application/json',
            )

        return web.json_response(self.serializer_class().dump(instance))
