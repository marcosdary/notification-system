import jwt
from secrets import token_hex

from api.constants import settings

class TokenService:
    def __init__(self):
        self._token = settings.TOKEN
    
    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self._token, "HS256")

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self._token, "HS256")
    

    
    