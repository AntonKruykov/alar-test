from marshmallow import fields

from apps.routes.serializers import RouteListSerializer, RouteItemSerializer


class RouteReportSerializer(RouteListSerializer):
    """Serializer for route report string."""

    username = fields.Function(lambda data: data.user.username)
    items = fields.List(fields.Nested(RouteItemSerializer))
