from api.schemas.base import BaseSchema

class PasswordResetSchema(BaseSchema):
    link: str
    