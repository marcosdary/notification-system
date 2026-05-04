from pydantic import RootModel
from typing import List

from app.schemas.email_notification_schema.read import EmailNotificationReadSchema

class ListEmailNotificationSchema(RootModel[List[EmailNotificationReadSchema]]): pass
