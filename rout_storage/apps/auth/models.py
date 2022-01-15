import peewee

from helpers.models import BaseModel


class AuthUser(BaseModel):
    """User model."""

    username = peewee.CharField(
        unique=True,
        index=True,
        max_length=100,
        null=False,
    )
    password = peewee.CharField(max_length=128)

    def token_payload(self):
        """Payload for jwt."""
        return {
            'user_id': self.id,
            'username': self.username,
        }
