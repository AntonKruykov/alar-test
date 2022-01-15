from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple

from aiohttp.web_request import Request
from jwt import encode as jwt_encode

from apps.auth.models import AuthUser


def encode_password(password: str) -> str:
    """Encode user password for store in db."""
    return str(hash(password))
