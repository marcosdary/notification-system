from datetime import datetime
from pydantic import field_serializer

from test.schemas.base import BaseSchema

class PasswordResetSchema(BaseSchema):
    subject: str = "Redefinição de Senha"
    link: str
    expiresAt: datetime

    @field_serializer("expiresAt", mode="plain")
    def serialize_date(self, value: datetime) -> str:
        return value.isoformat()