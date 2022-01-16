from marshmallow import Schema, fields


class PointSerializer(Schema):
    """Serializer for point."""

    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    latitude = fields.Integer(dump_only=True)
    longitude = fields.Integer(dump_only=True)


class RouteItemSerializer(Schema):
    """Serializer for route item."""

    point = fields.Nested(PointSerializer, dump_only=True)
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
