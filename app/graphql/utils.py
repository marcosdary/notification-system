from datetime import datetime

from app.schemas import ApiErrorSchema
from app.graphql.types import ApiResponseType


def build_response(success: bool, data=None, message: str = None, exc: Exception | None = None) -> ApiResponseType:
    """Constrói um ApiResponse padronizado.

    Args:
        success: Indica se a operação foi bem‑sucedida.
        data: Valor a ser retornado quando success=True.
        exc: Exceção capturada quando success=False.

    Returns:
        ApiResponse: objeto pronto para ser retornado ao cliente.
    """
    if success:
        return ApiResponseType(
            success=True, 
            data=data,
            message=message,
            timestamp=datetime.now().timestamp()
        )

    # Caso de erro
    return ApiResponseType(
        success=False,
        error=ApiErrorSchema(
            typeError=exc.__class__.__name__ if exc else "Error",
            errorName=str(exc) if exc else "",
            statusCode=getattr(exc, "status_code", 500),
        ),
        message=message,
        timestamp=datetime.now().timestamp()
    )