import peewee

from helpers.models import BaseModel


class RouteReport(BaseModel):
    """Model for route report record."""

    user_id = peewee.IntegerField(unique=True)
    username = peewee.CharField(unique=True, max_length=100)
    route_count = peewee.IntegerField(default=0)
    route_length = peewee.IntegerField(default=0)


class ReportUpdate(BaseModel):
    """Model for store update info."""

    report = peewee.IntegerField(unique=True)
    last_id = peewee.IntegerField(default=0)

