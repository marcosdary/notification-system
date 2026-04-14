import strawberry

from app.repositories import EmailNotificationRepository

from app.graphql.types import EmailNotificationType, ListEmailNotificationType, ApiResponseType, ApiErrorType
from app.graphql.utils import build_response
from app.graphql.permissions import ApiKeyPermission

@strawberry.type
class EmailNotificationQuery:
    
    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectById(self, idEmail: str) -> ApiResponseType[EmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
        
            return build_response(
                success=True,
                data= await email_notification_repository.select_by_id(idEmail)
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.field(permission_classes=[ApiKeyPermission])
    async def selectAll(self, page: int = 1, limit: int = 5) -> ApiResponseType[ListEmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()

            return build_response(
                success=True,
                data= await email_notification_repository.select_all(page=page, limit=limit)
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

