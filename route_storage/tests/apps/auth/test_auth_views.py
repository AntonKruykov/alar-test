import json

import pytest


class TestLoginView(object):

    @classmethod
    @pytest.fixture
    def url(cls, router_auth):
        return router_auth['login'].url_for()

    async def test_login(self, client, url, auth_user, auth_user_password, token):
        resp = await client.post(
            url,
            data=json.dumps(
                {
                    'username': auth_user.username,
                    'password': auth_user_password,
                },
            ),
        )
        assert resp.status == 200
        data = await resp.json()
        assert 'access_token' in data
        assert data['access_token'] == token

    async def test_incorrect_username(self, client, url):
        resp = await client.post(
            url,
            data=json.dumps(
                {
                    'username': 'test@gmail.com',
                    'password': 'test@gmail.com',
                },
            ),
        )
        assert resp.status == 400
        errors = await resp.json()
        assert errors['error']['username'] == ['Incorrect username.']

    async def test_incorrect_password(
        self,
        client,
        url, auth_user,
        auth_user_password,
    ):
        resp = await client.post(
            url,
            data=json.dumps(
                {
                    'username': auth_user.username,
                    'password': f'{auth_user_password}-salt',
                },
            ),
        )
        assert resp.status == 400
        errors = await resp.json()
        assert errors['error']['username'] == ['Incorrect password.']
