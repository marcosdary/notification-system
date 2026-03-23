from strawberry.experimental.pydantic import input as pydantic_input
import strawberry

from api.schemas.email_notification_schemas import (
    CreateEmailNotificationSchema
)

@pydantic_input(CreateEmailNotificationSchema, all_fields=True)
class EmailNotificationInput:
    pass




