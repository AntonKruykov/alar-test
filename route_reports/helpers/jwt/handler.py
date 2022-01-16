from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple

from aiohttp.web_request import Request
from jwt import encode as jwt_encode


DEFAULT_TOKEN_TTL = 720


class JWTHandler(object):
    """JWT HANDLER."""

    exp_key = 'exp'

    def __init__(
        self,
        request: Request,
        payload: Dict,
    ):
        self.settings = request.config_dict['settings']
        self.secret = self.settings['base']['secret']
        self.payload = payload
        self.request = request

    def create_token(self) -> str:
        """Create token for user."""

        access_payload: Dict = self.generate_payload()
        return self.encode_jwt(access_payload)

    def generate_payload(self, user_only: bool = False) -> Dict:
        """Create payload."""
        return {
            'token_type': 'access',
            self.exp_key: datetime.utcnow() + timedelta(
                minutes=self.settings.get(
                    'token', {},
                ).get('expire', DEFAULT_TOKEN_TTL),
            ),
            **self.payload,
        }

    def encode_jwt(self, payload: Dict) -> str:
        """Encode token."""
        return jwt_encode(payload, self.secret)
