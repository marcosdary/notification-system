import strawberry
from strawberry.exceptions import StrawberryGraphQLError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.email_notification_schema import EmailNotificationReadSchema
from app.graphql.inputs import EmailNotificationInput
from app.repositories import EmailNotificationRepository
from app.graphql.types import EmailNotificationType
from app.graphql.permissions import ApiKeyPermission

from app.exceptions import (
    EntityValidationError,
)


@strawberry.type
class EmailNotificationMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def create(
        self,
        info: strawberry.Info,
        schema: EmailNotificationInput
    ) -> EmailNotificationType:
        try:
            session: AsyncSession = info.context["session"]

            schema_pydantic = schema.to_pydantic()

            notification_repo = EmailNotificationRepository(session=session)
            data = await notification_repo.create(schema=schema_pydantic)
            await session.commit()
            return EmailNotificationReadSchema.model_validate(data)
        
        except EntityValidationError as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))

        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def delete(
        self,
        info: strawberry.Info,
        idEmail: str
    ) -> None:
        try:
            session: AsyncSession = info.context["session"]
            notification_repo = EmailNotificationRepository(session=session)
            await notification_repo.delete(idEmail=idEmail)
            await session.commit()
            return 

        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def deleteAll(
        self,
        info: strawberry.Info,
    ) -> None:
        try:
            session: AsyncSession = info.context["session"]
            notification_repo = EmailNotificationRepository(session=session)
            await notification_repo.delete_all()
            await session.commit()
            return 

        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))