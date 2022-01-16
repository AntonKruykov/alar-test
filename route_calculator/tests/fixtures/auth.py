import pytest

from helpers.jwt.handler import JWTHandler


@pytest.fixture
def jwt_factory(settings):
    """Factory for creating jwt."""
    async def create(user_payload):

        class FakeRequest(object):
            config_dict = {
                'settings': settings,
            }

        jwt_handler = JWTHandler(FakeRequest(), user_payload)
        access_payload = jwt_handler.generate_payload()
        return jwt_handler.encode_jwt(access_payload)

    return create


@pytest.fixture
async def token(jwt_factory):
    """Fixture for create jwt."""
    return await jwt_factory(
        {
            'user_id': 1,
            'username': 'test@test.te',
        }
    )
