import strawberry

from app.repositories import EmailNotificationRepository
from app.core import LOGGER as logger
from app.graphql.types import EmailNotificationType, ListEmailNotificationType, ApiResponseType, ApiErrorType
from app.graphql.utils import build_response
from app.graphql.permissions import ApiKeyPermission

@strawberry.type
class EmailNotificationQuery:
    
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectById(self, idEmail: str) -> ApiResponseType[EmailNotificationType, ApiErrorType]:
        try:
            mutation = "EmailNotificationQuery.selectById"
            email_notification_repository = EmailNotificationRepository()
            logger.info(
                "Selecionar as notificações por e-mail por ID.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_ID_START",
                    "mutation": mutation,
                    "layer": "graphql",
                    "notification_id": idEmail
                }
            )
            return build_response(
                success=True,
                data= await email_notification_repository.select_by_id(idEmail)
            )
        
        except Exception as exc:
            logger.exception(
                "Falha em selecionar o item por ID da notificação e-mail",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_ID_ERROR",
                    "mutation": mutation,
                    "layer": "graphql",
                }
            )
            return build_response(False, exc=exc)

    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectAll(self, page: int = 1, limit: int = 5) -> ApiResponseType[ListEmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
            mutation = "EmailNotificationQuery.selectAll"
            logger.info(
                "Selecionar as notificações por e-mail por page (página) e limit (limite).",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_ALL_START",
                    "layer": "graphql",
                    "mutation": mutation
                }
            )
            return build_response(
                success=True,
                data= await email_notification_repository.select_all(page=page, limit=limit)
            )
        
        except Exception as exc:
            logger.exception(
                "Falha em selecionar os itens da notificação e-mail por page (página) e limit (limite)",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_ALL_ERROR",
                    "mutation": mutation,
                    "error": str(exc),
                    "layer": "graphql",
                    "type_error": exc.__class__.__name__
                }
            )
            return build_response(False, exc=exc)

