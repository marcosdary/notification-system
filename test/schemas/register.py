from test.schemas.base import BaseSchema

class RegisterSchema(BaseSchema):
    subject: str = "Confirmação de Cadastro"
    link: str
    

