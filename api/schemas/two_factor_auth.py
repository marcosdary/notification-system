from pydantic import field_serializer
from datetime import datetime
from uuid import uuid4

from api.schemas.base import BaseSchema

class TwoFactorAuthSchema(BaseSchema):
    idTwoFAuth: str = str(uuid4())
    coding: int
    expiresAt: datetime

    @field_serializer("expiresAt", mode="plain")
    def serialize_dates(self, value: datetime) -> str:
        return value.strftime("%y-%m-%d %H:%M")
    


    