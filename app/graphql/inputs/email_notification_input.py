from strawberry.experimental.pydantic import input as pydantic_input

from app.schemas.email_notification_schema import (
    CreateEmailNotificationSchema
)

@pydantic_input(CreateEmailNotificationSchema, all_fields=True)
class EmailNotificationInput:
    pass




