import json
from typing import Dict

from aiohttp import web
from marshmallow import ValidationError


class BaseView(web.View):

    @property
    def serializer_class(self):
        raise NotImplementedError

    @property
    def database(self):
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
