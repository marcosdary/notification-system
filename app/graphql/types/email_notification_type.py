from strawberry.experimental.pydantic import type as pydantic_type

from app.schemas.email_notification_schema import (
    EmailNotificationReadSchema, 
    ListEmailNotificationSchema,
    EmailNotificationFilterBySchema
)

@pydantic_type(EmailNotificationReadSchema, all_fields=True)
class EmailNotificationType:
    pass 

@pydantic_type(ListEmailNotificationSchema, all_fields=True)
class ListEmailNotificationType:
    pass

