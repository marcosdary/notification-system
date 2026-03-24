from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from api.config import settings
from api.exceptions import (
    InvalidFieldsException
)

class ApiKeyPermission(BasePermission):

    def __init__(self):
        super().__init__()

    def has_permission(self, source, info, **kwargs):
        try:
            from json import dumps
            headers: dict = info.context["request"].headers
        
            auth = headers.get("Authorization")

            if not auth:
                raise InvalidFieldsException("Não possui a chave de API. Acesso negado.")
            
            try:
                scheme, token = auth.split(" ")

                if scheme.lower() != "bearer":
                    return False
                
            except Exception as exc:
                return False

            if token != settings.TOKEN:
                raise InvalidFieldsException("A chave de API é inválida ou incorreta. Acesso negado.")
            
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })