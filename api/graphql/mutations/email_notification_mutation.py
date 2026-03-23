import strawberry

from api.graphql.inputs.email_notification_input import (
    EmailNotificationInput
)
from api.tasks.email_task import process_email_notification
from api.repositories import EmailNotificationRepository
from api.graphql.types import EmailNotificationType, ApiResponseType, ApiErrorType
from api.graphql.utils import build_response

@strawberry.type
class EmailNotificationMutation:
    
    @strawberry.mutation
    def newEmailNotification(self, schema: EmailNotificationInput) -> ApiResponseType[EmailNotificationType, ApiErrorType]:
        try:
            data = schema.to_pydantic()
            notification_repo = EmailNotificationRepository()
            response = notification_repo.create(schema=data)
            data.idEmail = response.idEmail
            process_email_notification.delay(data.model_dump())
            return build_response(
                success=True,
                data=response
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def deleteEmailNotification(self, idEmail: str) -> ApiResponseType[None, ApiErrorType]:
        try:
            notification_repo = EmailNotificationRepository()
    
            return build_response(
                success=True,
                data=notification_repo.delete(idEmail=idEmail)
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def deleteAllEmailNotification(self) -> ApiResponseType[None, ApiErrorType]:
        try:
            notification_repo = EmailNotificationRepository()
    
            return build_response(
                success=True,
                data=notification_repo.delete_all()
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)