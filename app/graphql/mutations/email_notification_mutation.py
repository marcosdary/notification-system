import strawberry

from app.graphql.inputs.email_notification_input import EmailNotificationInput
from app.core import LOGGER as logger
from app.tasks.email_task import process_email_notification
from app.repositories import EmailNotificationRepository
from app.graphql.types import EmailNotificationType, ApiResponseType, ApiErrorType
from app.graphql.utils import build_response
from app.graphql.permissions import ApiKeyPermission


@strawberry.type
class EmailNotificationMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def create(
        self,
        schema: EmailNotificationInput
    ) -> ApiResponseType[EmailNotificationType, ApiErrorType]:
        try:
            mutation = "EmailNotificationMutation.create"
            logger.info(
                "A criação do e-mail foi iniciada",
                extra={
                    "event": "EMAIL_NOTIFICATION_CREATE_START",
                    "mutation": mutation,
                    "layer": "graphql"
                }
            )

            schema_pydantic = schema.to_pydantic()

            notification_repo = EmailNotificationRepository()
            data = await notification_repo.create(schema=schema_pydantic)

            notification_id = data.idEmail

            logger.info(
                "E-mail criado com sucesso",
                extra={
                    "event": "EMAIL_NOTIFICATION_CREATED_SUCCESS",
                    "notification_id": data.idEmail,
                    "mutation": mutation,
                    "layer": "graphql"
                }
            )

            task = process_email_notification.delay(data.model_dump())

            logger.info(
                "Tarefa despachada para Celery", 
                extra={
                    "event": "CELERY_EMAIL_NOTIFICATION_DISPATCHED",
                    "notification_id": notification_id,
                    "task": task.id,
                    "mutation": mutation,
                    "layer": "graphql"
                }
            )

            return build_response(
                success=True,
                data=data
            )

        except Exception as exc:
            logger.exception(
                "Falha na criação do e-mail",
                extra={
                    "event": "EMAIL_NOTIFICATION_CREATE_ERROR",
                    "mutation": mutation,
                    "layer": "graphql",
                    "error": str(exc),
                    "type_error": exc.__class__.__name__
                }
            )
            return build_response(success=False, exc=Exception("Erro interno ao criar notificação"))

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def delete(
        self,
        idEmail: str
    ) -> ApiResponseType[None, ApiErrorType]:
        try:
            mutation = "EmailNotificationMutation.delete"
            logger.info(
                "A deleção do e-mail foi iniciada",
                extra={
                    "event": "EMAIL_NOTIFICATION_DELETE_START",
                    "mutation": mutation,
                    "layer": "graphql"
                }
            )

            notification_repo = EmailNotificationRepository()
            result = await notification_repo.delete(idEmail=idEmail)

            logger.info(
                "A deleção foi concluída com sucesso",
                extra={
                    "event": "EMAIL_NOTIFICATION_DELETE_SUCCESS",
                    "notification_id": idEmail,
                    "mutation": mutation,
                    "layer": "graphql"
                }
            )

            return build_response(
                success=True,
                data=result
            )

        except Exception as exc:
            logger.exception(
                "Erro ao apagar a notificação de e-mail",
                extra={
                    "event": "EMAIL_NOTIFICATION_DELETE_ERROR",
                    "notification_id": idEmail,
                    "mutation": mutation,
                    "layer": "graphql",
                    "error": str(exc),
                    "type_error": exc.__class__.__name__,
                }
            )
            return build_response(success=False, exc=Exception("Erro interno ao excluir notificação"))

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def deleteAll(
        self
    ) -> ApiResponseType[None, ApiErrorType]:
        try:
            mutation = "EmailNotificationMutation.deleteAll"
            logger.info(
                "A deleção de todos foi inciada.",
                extra={
                    "event": "EMAIL_NOTIFICATION_DELETE_ALL_START",
                    "mutation": mutation,
                    "layer": "graphql"
                }
            )

            notification_repo = EmailNotificationRepository()
            result = await notification_repo.delete_all()

            logger.info(
                "A deleção foi concluída com sucesso.",
                extra={
                    "event": "EMAIL_NOTIFICATION_DELETE_ALL_SUCCESS",
                    "mutation": mutation,
                    "layer": "graphql"
                }
            )

            return build_response(
                success=True,
                data=result
            )

        except Exception as exc:
            logger.exception(
                "Erro ao apagar todos os registros de notificação.",
                extra={
                    "event": "EMAIL_NOTIFICATION_DELETE_ALL_ERROR",
                    "mutation": mutation,
                    "layer": "graphql",
                    "error": str(exc),
                    "type_error": exc.__class__.__name__,
                }
            )
            return build_response(success=False, exc=Exception("Internal error while deleting all notifications"))