from test.schemas.base import BaseSchema

class PasswordChangeSchema(BaseSchema):
    subject: str = "Confirmação de Alteração de Senha"
    pass