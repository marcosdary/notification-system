from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.core.constants import SendType, StatusEmail

class EmailNotificationFilterBySchema(BaseModel):
    status: Optional[StatusEmail] = None
    sendType: Optional[SendType] = None