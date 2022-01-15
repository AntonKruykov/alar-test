import json

from aiohttp import web

from apps.auth.models import AuthUser
from apps.auth.serializsers import AuthSerializer
from apps.auth.utils import encode_password
from helpers.jwt.handler import JWTHandler
from helpers.views import BaseView


class LoginView(BaseView):
    """Login view."""

    serializer_class = AuthSerializer

    async def post(self):
        """Authorize user and return jwt."""
        data = await self.validate_data()
        user = await self.get_user(data['username'])
        self.check_password(user, data['password'])
        access_token = self.create_token(user)
        return web.json_response(
            {
                'access_token': access_token,
            }
        )

    async def get_user(self, username: str) -> AuthUser:
        """Retrieve user from db by username."""
        try:
            return await self.database.get(
                AuthUser,
                AuthUser.username == username,
            )
        except AuthUser.DoesNotExist:
            raise web.HTTPBadRequest(
                text=json.dumps({
                    'error': {
                        'username': ['Incorrect username.'],
                    },
                }),
                content_type='application/json',
            )

    @classmethod
    def check_password(cls, user: AuthUser, password) -> None:
        """Check if password valid for user."""
        if encode_password(password) != user.password:
            raise web.HTTPBadRequest(
                text=json.dumps({
                    'error': {
                        'username': ['Incorrect password.'],
                    },
                }),
                content_type='application/json',
            )

    def create_token(self, user: AuthUser) -> str:
        """Generate jwt for authorized user."""
        jwt_handler = JWTHandler(self.request, user.token_payload())
        return jwt_handler.create_token()
