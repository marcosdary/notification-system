from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4

class NotificationSchema(BaseModel):
    idSend: str = str(uuid4())
    typeSend: str
    templateName: str
    info: dict
    function: str
    createdAt: datetime = datetime.now()
    endIn: datetime = datetime.now()




