import json
import re
from typing import Callable, Tuple, Iterable

import jwt
from aiohttp import web


def jwt_middleware(  # noqa: C901
    secret_or_pub_key: str,
    whitelist: Tuple = tuple,
) -> Callable:
    """JWT middleware.

    For more information read: https://en.wikipedia.org/wiki/JSON_Web_Token

    """
    if not (secret_or_pub_key and isinstance(secret_or_pub_key, str)):
        raise RuntimeError(
            'secret or public key should be provided for correct work',
        )

    @web.middleware
    async def _middleware(
        request: web.Request,
        handler: Callable,
    ) -> web.Resource:

        if check_request(request, whitelist) or request.method == 'OPTIONS':
            # skip validate requets for CORS
            # if request method equal 'OPTIONS'
            return await handler(request)

        token = None

        if 'Authorization' in request.headers:
            try:
                header = request.headers.get('Authorization', '').strip()
            except ValueError:
                raise web.HTTPUnauthorized(
                    text=json.dumps({
                        'error': ['Invalid authorization header'],
                    }),
                    content_type='application/json',
                )
            scheme, token = header.split(' ')

            if not re.match('Bearer', scheme):
                raise web.HTTPUnauthorized(
                    text=json.dumps({
                        'error': ['Invalid token scheme'],
                    }),
                    content_type='application/json',
                )

        if not token:
            raise web.HTTPUnauthorized(
                text=json.dumps({
                    'error': ['Missing authorization token'],
                }),
                content_type='application/json',
            )

        if not isinstance(token, bytes):
            token = token.encode()

        try:
            decoded = jwt.decode(token, secret_or_pub_key)
        except jwt.InvalidTokenError:
            raise web.HTTPUnauthorized(
                text=json.dumps({
                    'error': ['Invalid token'],
                }),
                content_type='application/json',
            )

        request['user'] = decoded

        return await handler(request)

    return _middleware


def check_request(request: web.Resource, entries: Iterable) -> bool:
    """Check access to endpoint."""
    for pattern in entries:
        if re.match(pattern, request.path):
            return True
    return False
