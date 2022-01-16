from marshmallow import Schema, fields


class RouteReportSerializer(Schema):
    """Serializer for report record."""

    id = fields.Integer()
    user_id = fields.Integer()
    username = fields.String()
    route_count = fields.Integer()
    route_length = fields.Integer()
