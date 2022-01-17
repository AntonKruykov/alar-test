import peewee

from apps.auth.models import AuthUser
from helpers.models import BaseModel


class Point(BaseModel):
    """Model for point."""

    name = peewee.CharField(
        unique=True,
        index=True,
        max_length=100,
        null=False,
    )
    latitude = peewee.IntegerField(null=False)
    longitude = peewee.IntegerField(null=False)


class Route(BaseModel):
    """Model for route."""

    user = peewee.ForeignKeyField(AuthUser)
    name = peewee.CharField(max_length=100, null=False)


class RouteItem(BaseModel):
    """Model for point of route."""

    route = peewee.ForeignKeyField(Route, backref='items')
    point = peewee.ForeignKeyField(Point)
    order = peewee.IntegerField(null=True)