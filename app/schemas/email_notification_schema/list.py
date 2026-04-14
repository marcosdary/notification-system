from typing import List, Optional

from app.schemas.email_notification_schema.base import BaseEmailNotificationSchema
from app.schemas.email_notification_schema.read import ReadEmailNotificationSchema

class ListEmailNotificationSchema(BaseEmailNotificationSchema):
    notifications: Optional[List[ReadEmailNotificationSchema]] | None = [] 