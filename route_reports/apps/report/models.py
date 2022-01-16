import peewee

from helpers.models import BaseModel


class RouteReport(BaseModel):

    user_id = peewee.IntegerField(unique=True)
    username = peewee.CharField(unique=True, max_length=100)
    route_count = peewee.IntegerField(default=0)
    route_length = peewee.IntegerField(default=0)
