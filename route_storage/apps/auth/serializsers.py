from marshmallow import Schema, fields


class AuthUserSerializer(Schema):
    """User login form serializer."""

    username = fields.Email(required=True)
    password = fields.String(required=True)