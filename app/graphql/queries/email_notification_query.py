import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.exceptions import StrawberryGraphQLError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import EmailNotificationRepository

from app.schemas.email_notification_schema import EmailNotificationReadSchema, ListEmailNotificationSchema
from app.graphql.types import EmailNotificationType, ListEmailNotificationType
from app.graphql.inputs import PaginationInput, EmailNotificationFilterByInput
from app.graphql.permissions import ApiKeyPermission

@strawberry.type
class EmailNotificationQuery:
    
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectById(self, info: strawberry.Info, idEmail: str) -> EmailNotificationType:
        try:
            session: AsyncSession = info.context["session"]
            email_notification_repository = EmailNotificationRepository(session=session)
            data = await email_notification_repository.select_by_id(idEmail)
            return EmailNotificationReadSchema.model_validate(data)
        
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc))

    @strawberry.field(permission_classes=[ApiKeyPermission], extensions=[InputMutationExtension()])
    async def selectAll(
        self, info: strawberry.Info,  
        pagination: PaginationInput,
        filterBy: EmailNotificationFilterByInput = None
    ) -> ListEmailNotificationType:
        try:
            session: AsyncSession = info.context["session"]
            email_notification_repository = EmailNotificationRepository(session=session)
            filter_by = filterBy.to_pydantic() if filterBy else None
            pagination = pagination.to_pydantic()
            rows = await email_notification_repository.select_filter_all(filter_by=filter_by, pagination=pagination)
            return ListEmailNotificationSchema.model_validate(rows)
        
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc))
        
   



