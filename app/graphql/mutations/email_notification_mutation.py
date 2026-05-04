import strawberry
from strawberry.exceptions import StrawberryGraphQLError

from app.graphql.inputs import EmailNotificationInput
from app.core import LOGGER as logger
from app.tasks.email_task import process_email_notification
from app.repositories import EmailNotificationRepository
from app.graphql.types import EmailNotificationType
from app.graphql.permissions import ApiKeyPermission


@strawberry.type
class EmailNotificationMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def create(
        self,
        schema: EmailNotificationInput
    ) -> EmailNotificationType:
        try:
            
            schema_pydantic = schema.to_pydantic()

            notification_repo = EmailNotificationRepository()
            data = await notification_repo.create(schema=schema_pydantic)

            notification_id = data.idEmail
            task = process_email_notification.delay(data.model_dump())

            return data

        except Exception as exc:
            raise StrawberryGraphQLError(message="Erro interno ao criar notificação")

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def delete(
        self,
        idEmail: str
    ) -> None:
        try:
            notification_repo = EmailNotificationRepository()
            await notification_repo.delete(idEmail=idEmail)
            return 

        except Exception as exc:
            raise StrawberryGraphQLError("Erro interno ao excluir notificação")

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def deleteAll(
        self
    ) -> None:
        try:
            notification_repo = EmailNotificationRepository()
            await notification_repo.delete_all()
            return 

        except Exception as exc:
            raise StrawberryGraphQLError("Internal error while deleting all notifications")