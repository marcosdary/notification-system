from strawberry.experimental.pydantic import input as pydantic_input

from api.schemas.email_notification_schemas import (
    CreateEmailNotificationSchema
)

@pydantic_input(CreateEmailNotificationSchema, all_fields=True)
class EmailNotificationInput:
    pass




