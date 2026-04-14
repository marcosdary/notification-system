import strawberry

from app.graphql.inputs.email_notification_input import (
    EmailNotificationInput
)
from app.tasks.email_task import process_email_notification
from app.repositories import EmailNotificationRepository
from app.graphql.types import EmailNotificationType, ApiResponseType, ApiErrorType
from app.graphql.utils import build_response
from app.graphql.permissions import ApiKeyPermission

@strawberry.type
class EmailNotificationMutation:
    
    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def create(self, schema: EmailNotificationInput) -> ApiResponseType[EmailNotificationType, ApiErrorType]:
        try:
            schema = schema.to_pydantic()
           
            notification_repo = EmailNotificationRepository()
            data = await notification_repo.create(schema=schema)
            process_email_notification.delay(data.model_dump())
            return build_response(
                success=True,
                data=data
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def delete(self, idEmail: str) -> ApiResponseType[None, ApiErrorType]:
        try:
            notification_repo = EmailNotificationRepository()
    
            return build_response(
                success=True,
                data= await notification_repo.delete(idEmail=idEmail)
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def deleteAllEmailNotification(self) -> ApiResponseType[None, ApiErrorType]:
        try:
            notification_repo = EmailNotificationRepository()
    
            return build_response(
                success=True,
                data= await notification_repo.delete_all()
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)