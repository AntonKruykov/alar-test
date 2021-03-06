from marshmallow import Schema, fields


class PointSerializer(Schema):
    """Serializer for point."""

    id = fields.Integer()
    name = fields.String()
    latitude = fields.Integer()
    longitude = fields.Integer()


class RouteItemSerializer(Schema):
    """Serializer for route item."""

    point = fields.Nested(PointSerializer, allow_none=True)
    point_id = fields.Integer(required=True)
    order = fields.Integer(required=True)


class RouteListSerializer(Schema):
    """Serializer for route list."""

    id = fields.Integer()
    name = fields.String()
    user_id = fields.Integer()


class RouteDetailSerializer(RouteListSerializer):
    """Serializer for route."""

    items = fields.List(fields.Nested(RouteItemSerializer))
