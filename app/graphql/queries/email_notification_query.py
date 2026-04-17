import strawberry
from datetime import datetime

from app.repositories import EmailNotificationRepository
from app.constants import StatusEmail, SendType
from app.core import LOGGER as logger
from app.graphql.types import EmailNotificationType, ListEmailNotificationType, ApiResponseType, ApiErrorType
from app.graphql.utils import build_response
from app.graphql.inputs import PaginationInput, DateRangeInput
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
    async def selectAll(self, pagination: PaginationInput) -> ApiResponseType[ListEmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
            pagination = pagination.to_pydantic()

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
                data= await email_notification_repository.select_filter_all(pagination=pagination)
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
        
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectByStatus(self, status: StatusEmail, pagination: PaginationInput) -> ApiResponseType[ListEmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
            pagination = pagination.to_pydantic()

            mutation = "EmailNotificationQuery.selectByStatus"
            logger.info(
                "Selecionar as notificações por e-mail por paginação (página, limite) e status.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_STATUS_START",
                    "layer": "graphql",
                    "mutation": mutation
                }
            )
            return build_response(
                success=True,
                data= await email_notification_repository.select_filter_all(pagination=pagination, status_email=status)
            )
        
        except Exception as exc:
            logger.exception(
                "Falha em selecionar os itens da notificação e-mail por paginação (página, limite) e status",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_STATUS_ERROR",
                    "mutation": mutation,
                    "error": str(exc),
                    "layer": "graphql",
                    "type_error": exc.__class__.__name__
                }
            )
            return build_response(False, exc=exc)

    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectBySendType(self, sendType: SendType, pagination: PaginationInput) -> ApiResponseType[ListEmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
            pagination = pagination.to_pydantic()

            mutation = "EmailNotificationQuery.selectBySendType"
            logger.info(
                "Selecionar as notificações por e-mail por paginação (página, limite) e tipo de envio.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_SEND_TYPE_START",
                    "layer": "graphql",
                    "mutation": mutation
                }
            )
            return build_response(
                success=True,
                data= await email_notification_repository.select_filter_all(pagination=pagination, send_type=sendType)
            )
        
        except Exception as exc:
            logger.exception(
                "Falha em selecionar os itens da notificação e-mail por paginação (página, limite) e tipo de envio.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_STATUS_ERROR",
                    "mutation": mutation,
                    "error": str(exc),
                    "layer": "graphql",
                    "type_error": exc.__class__.__name__
                }
            )
            return build_response(False, exc=exc)
        
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectByDateRange(self, dateRange: DateRangeInput, pagination: PaginationInput) -> ApiResponseType[ListEmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
            pagination = pagination.to_pydantic()
            dateRange = dateRange.to_pydantic()

            mutation = "EmailNotificationQuery.selectByDateRange"
            logger.info(
                "Selecionar as notificações por e-mail por paginação (página, limite) e faixa de datas.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_DATA_RANGE_START",
                    "layer": "graphql",
                    "mutation": mutation
                }
            )
            return build_response(
                success=True,
                data= await email_notification_repository.select_filter_all(pagination=pagination, date_range=dateRange)
            )
        
        except Exception as exc:
            logger.exception(
                "Falha em selecionar os itens da notificação e-mail por paginação (página, limite) e faixa de datas.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_DATA_RANGE_ERROR",
                    "mutation": mutation,
                    "error": str(exc),
                    "layer": "graphql",
                    "type_error": exc.__class__.__name__
                }
            )
            return build_response(False, exc=exc)
        
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectByCreatedAfter(self, date: datetime, pagination: PaginationInput) -> ApiResponseType[ListEmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
            pagination = pagination.to_pydantic()

            mutation = "EmailNotificationQuery.selectByCreatedAfter"
            logger.info(
                "Selecionar as notificações por e-mail por paginação (página, limite) e data.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_DATA_START",
                    "layer": "graphql",
                    "mutation": mutation
                }
            )
            return build_response(
                success=True,
                data= await email_notification_repository.select_filter_all(pagination=pagination, date=date)
            )
        
        except Exception as exc:
            logger.exception(
                "Falha em selecionar os itens da notificação e-mail por paginação (página, limite) e data.",
                extra={
                    "event": "EMAIL_NOTIFICATION_QUERY_SELECT_BY_DATA_ERROR",
                    "mutation": mutation,
                    "error": str(exc),
                    "layer": "graphql",
                    "type_error": exc.__class__.__name__
                }
            )
            return build_response(False, exc=exc)



