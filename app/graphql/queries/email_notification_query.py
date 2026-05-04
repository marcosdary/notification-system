import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.exceptions import StrawberryGraphQLError
from datetime import datetime

from app.repositories import EmailNotificationRepository

from app.core import LOGGER as logger
from app.graphql.types import EmailNotificationType, ListEmailNotificationType
from app.graphql.inputs import PaginationInput, EmailNotificationFilterByInput
from app.graphql.permissions import ApiKeyPermission

@strawberry.type
class EmailNotificationQuery:
    
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectById(self, idEmail: str) -> EmailNotificationType:
        try:
            email_notification_repository = EmailNotificationRepository()
            return await email_notification_repository.select_by_id(idEmail)
        
        except Exception as exc:
            
            raise StrawberryGraphQLError(str(exc))

    @strawberry.field(permission_classes=[ApiKeyPermission], extensions=[InputMutationExtension()])
    async def selectAll(self, filterBy: EmailNotificationFilterByInput, pagination: PaginationInput) -> ListEmailNotificationType:
        try:
            email_notification_repository = EmailNotificationRepository()
            pagination = pagination.to_pydantic()
            return await email_notification_repository.select_filter_all(pagination=pagination)
        
        except Exception as exc:

            raise StrawberryGraphQLError(str(exc))
        
   



