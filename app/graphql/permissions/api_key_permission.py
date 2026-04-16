from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError
from time import time

from app.config import settings
from app.core import LOGGER as logger
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

            logger.info(
                "Iniciar o processo de checagem da Api Key.",
                extra={
                    "event": "API_KEY_PERMISSION_START",
                    "permission": "ApiKeyPermission",
                    "layer": "graphql",
                    "api_key": api_key
                }
            )

            start = time()

            if not api_key:
                raise InvalidFieldsException("Não possui a chave de API. Acesso negado.")  

            if api_key != settings.API_KEY:
                raise InvalidFieldsException("A chave de API é inválida ou incorreta. Acesso negado.")
            
            execution = time() - start

            logger.info(
                "Verificação concluída com sucesso.",
                extra={
                    "event": "API_KEY_PERMISSION_SUCCESS",
                    "execution_time": execution,
                    "layer": "graphql"
                }
            )
            
            return True
        except Exception as exc:

            logger.exception(
                "Erro na verificação da Api Key.",
                extra={
                    "event": "API_KEY_PERMISSION_ERROR",
                    "error": str(exc),
                    "layer": "graphql",
                    "type_error": exc.__class__.__name__,
                }
            )
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })