from strawberry.experimental.pydantic import type as pydantic_type

from api.schemas.email_notification_schemas import ReadEmailNotificationSchema

@pydantic_type(ReadEmailNotificationSchema, all_fields=True)
class EmailNotificationType:
    pass 

