import peewee
import peewee_async

database = peewee_async.PooledPostgresqlDatabase(None)


class BaseModel(peewee.Model):
    """Base model class."""

    class Meta:
        """Base model options."""

        database = database
