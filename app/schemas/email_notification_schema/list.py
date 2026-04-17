from typing import List, Optional

from app.schemas.email_notification_schema.base import BaseEmailNotificationSchema
from app.schemas.email_notification_schema.read import ReadEmailNotificationSchema

class ListEmailNotificationSchema(BaseEmailNotificationSchema):
    items: Optional[List[ReadEmailNotificationSchema]] | None = [] 
    total: int | None = 0
    page: int
    limit: int
    hasNextPage: bool | None = True