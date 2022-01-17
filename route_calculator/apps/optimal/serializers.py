from marshmallow import Schema, fields


class PointSerializer(Schema):
    """Serializer for point."""

    id = fields.Integer()
    name = fields.String()
    latitude = fields.Integer()
    longitude = fields.Integer()


class RouteItemSerializer(Schema):
    """Serializer for route item."""

    point = fields.Nested(PointSerializer)
    point_id = fields.Integer(dump_only=True)
    order = fields.Integer(dump_only=True)


class RouteSerializer(Schema):
    """Serializer for route list."""

    name = fields.String()
    user_id = fields.Integer()
    items = fields.List(fields.Nested(RouteItemSerializer))


class CreateOptimalRouteSerializer(RouteSerializer):
    """Serializer for create optimal route endpoint."""

    point_a = fields.Nested(PointSerializer)
    point_b = fields.Nested(PointSerializer)
