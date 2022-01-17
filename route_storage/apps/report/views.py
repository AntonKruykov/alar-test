from typing import List

from peewee import Query

from apps.auth.models import AuthUser
from apps.report.serializsers import RouteReportSerializer
from apps.routes.models import Route, RouteItem, Point
from helpers.views import BaseListView


class RouteReportDataView(BaseListView):

    serializer_class = RouteReportSerializer

    async def get_query(self) -> Query:
        id_gt = self.request.rel_url.query.get('id__gt', 0)
        return Route.select(
            Route,
            AuthUser,
        ).join(
            AuthUser,
            on=(Route.user == AuthUser.id),
        ).where(
            Route.id > id_gt,
        ).order_by(
            Route.id,
        )

    async def execute_list_query(self, query: Query) -> List:

        return await self.database.prefetch(
            query,
            RouteItem.select(
                RouteItem,
                Point,
            ).join(
                Point,
                on=(RouteItem.point == Point.id),
            )
        )
