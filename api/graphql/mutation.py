import strawberry

from api.constants import TypeSend, Templates
from api.schemas import NotificationSchema
from api.graphql.inputs import (
    PasswordChangeInput,
    PasswordResetInput,
    TwoFactorAuthInput,
    RegisterInput
)
from api.queues import NotificationQueue
from api.graphql.types import NotificationType, ApiResponseType, ApiErrorType
from api.graphql.utils import build_response

@strawberry.type
class Mutation:
    
    @strawberry.mutation
    def register(self, schema: RegisterInput) -> ApiResponseType[NotificationType, ApiErrorType]:
        try:
            register = schema.to_pydantic()
            notification_schema = NotificationSchema(
                info=register.model_dump()
            )
            notification_queue = NotificationQueue()
            notification_queue.add_notification(notification_schema)
            return build_response(
                success=True,
                data=notification_schema
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def passwordReset(self, schema: PasswordResetInput) -> ApiResponseType[NotificationType, ApiErrorType]:
        try:
            password_reset = schema.to_pydantic()
            notification_schema = NotificationSchema(
                info=password_reset.model_dump(),
                typeSend=TypeSend.PASSWORD_RESET,
                templateName=Templates.PASSWORD_RESET
            )
            notification_queue = NotificationQueue()
            notification_queue.add_notification(notification_schema)
            return build_response(
                success=True,
                data=notification_schema
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def passwordChange(self, schema: PasswordChangeInput) -> ApiResponseType[NotificationType, ApiErrorType]:
        try:
            password_change = schema.to_pydantic()
            notification_schema = NotificationSchema(
                info=password_change.model_dump(),
                typeSend=TypeSend.PASSWORD_CHANGE,
                templateName=Templates.PASSWORD_CHANGE
            )
            notification_queue = NotificationQueue()
            notification_queue.add_notification(notification_schema)
            return build_response(
                success=True,
                data=notification_schema
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def twoFactorAuth(self, schema: TwoFactorAuthInput) -> ApiResponseType[NotificationType, ApiErrorType]:
        try:
            two_factor_auth = schema.to_pydantic()
            notification_schema = NotificationSchema(
                info=two_factor_auth.model_dump(),
                typeSend=TypeSend.TWO_FACTOR_AUTH,
                templateName=Templates.TWO_F_AUTH
            )
            notification_queue = NotificationQueue()
            notification_queue.add_notification(notification_schema)
            return build_response(
                success=True,
                data=notification_schema
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

