from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.config import settings
from app.exceptions import (
    InvalidFieldsException
)

class ApiKeyPermission(BasePermission):

    def __init__(self):
        super().__init__()

    def has_permission(self, source, info, **kwargs):
        try:
            headers: dict = info.context["request"].headers
            api_key = headers.get("x-api-key")

            if not api_key:
                raise InvalidFieldsException("Não possui a chave de API. Acesso negado.")  

            if api_key != settings.API_KEY:
                raise InvalidFieldsException("A chave de API é inválida ou incorreta. Acesso negado.")
            
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })