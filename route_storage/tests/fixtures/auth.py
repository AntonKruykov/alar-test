import pytest

from apps.auth.models import AuthUser

from apps.auth.utils import encode_password
from helpers.jwt.handler import JWTHandler


@pytest.fixture
async def auth_user(object_factory, auth_user_password) -> AuthUser:
    """Fixture for create auth user object."""
    return await object_factory(
        AuthUser,
        username='test_user_name@test.te',
        password=encode_password(auth_user_password),
    )


@pytest.fixture
def auth_user_password() -> str:
    """Password of the auth_user."""
    return 'passw0rd'


@pytest.fixture
def jwt_factory(db, settings):
    """Factory for creating jwt."""
    async def create(user: AuthUser):

        class FakeRequest(object):
            config_dict = {
                'objects': db,
                'settings': settings,
            }



        jwt_handler = JWTHandler(FakeRequest(), user.token_payload())
        access_payload = jwt_handler.generate_payload()
        return jwt_handler.encode_jwt(access_payload)

    return create


@pytest.fixture
async def token(jwt_factory, auth_user):
    """Fixture for create auth user token."""
    return await jwt_factory(auth_user)
