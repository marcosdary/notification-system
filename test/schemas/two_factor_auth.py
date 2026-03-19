from pydantic import field_serializer
from datetime import datetime

from api.schemas.base import BaseSchema

class TwoFactorAuthSchema(BaseSchema):
    subject: str = "Verificação de 2 fatores"
    code: str
    expiresAt: datetime

    @field_serializer("expiresAt", mode="plain")
    def serialize_dates(self, value: datetime) -> str:
        return value.strftime("%y-%m-%d %H:%M")
    


    