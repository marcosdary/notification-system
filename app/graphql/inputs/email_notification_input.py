from strawberry.experimental.pydantic import input as pydantic_input

from app.schemas.email_notification_schema import (
    EmailNotificationCreateSchema,
    EmailNotificationFilterBySchema
)

@pydantic_input(EmailNotificationCreateSchema, all_fields=True)
class EmailNotificationInput:
    pass



@pydantic_input(EmailNotificationFilterBySchema, all_fields=True)
class EmailNotificationFilterByInput:
    pass


