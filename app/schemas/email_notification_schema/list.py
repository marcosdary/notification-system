from typing import List, Optional

from app.schemas.email_notification_schema.base import EmailNotificationBaseSchema
from app.schemas.email_notification_schema.read import EmailNotificationReadSchema

class ListEmailNotificationSchema(EmailNotificationBaseSchema):
    items: Optional[List[EmailNotificationReadSchema]] | None = [] 
    total: int | None = 0
    page: int
    limit: int
    hasNextPage: bool | None = True