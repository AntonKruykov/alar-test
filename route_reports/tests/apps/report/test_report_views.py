import pytest


class TestRouteReportView(object):

    @pytest.fixture
    def url(self, router_report):
        return router_report['routes'].url_for()

    async def test_report(self, client, url, token, report_record):
        resp = await client.get(
            url,
            headers={
                'Authorization': 'Bearer {0}'.format(token),
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data['count'] == 1
