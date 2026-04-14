from strawberry.experimental.pydantic import type as pydantic_type

from app.schemas.email_notification_schema import (
    ReadEmailNotificationSchema, 
    ListEmailNotificationSchema
)

@pydantic_type(ReadEmailNotificationSchema, all_fields=True)
class EmailNotificationType:
    pass 

@pydantic_type(ListEmailNotificationSchema, all_fields=True)
class ListEmailNotificationType:
    pass