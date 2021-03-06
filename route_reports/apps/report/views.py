from apps.report.models import RouteReport
from apps.report.serializers import RouteReportSerializer
from helpers.views import BaseListView


class RouteReportView(BaseListView):
    """Report."""

    serializer_class = RouteReportSerializer
    query = RouteReport.select()
