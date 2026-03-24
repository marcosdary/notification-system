import strawberry
from typing import List

from api.repositories import EmailNotificationRepository

from api.graphql.types import EmailNotificationType, ApiResponseType, ApiErrorType
from api.graphql.utils import build_response
from api.graphql.permissions import ApiKeyPermission

@strawberry.type
class EmailNotificationQuery:
    
    @strawberry.field(permission_classes=[ApiKeyPermission])
    def selectById(self, idEmail: str) -> ApiResponseType[EmailNotificationType, ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()
        
            return build_response(
                success=True,
                data=email_notification_repository.select_by_id(idEmail)
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.field(permission_classes=[ApiKeyPermission])
    def selectAll(self) -> ApiResponseType[List[EmailNotificationType], ApiErrorType]:
        try:
            email_notification_repository = EmailNotificationRepository()

            return build_response(
                success=True,
                data=email_notification_repository.select_all()
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

