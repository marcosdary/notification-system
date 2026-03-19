from sqlalchemy import Column, VARCHAR, Enum, TIMESTAMP, Text, func 
from uuid import uuid4

from api.models.base import BaseModel
from api.constants import TypeSend, Status

class NotificationsModel(BaseModel):

    __tablename__ = "notifications"

    idSend = Column(VARCHAR(255), primary_key=True, default=lambda: str(uuid4()))
    info = Column(Text, nullable=False)
    typeSend = Column(Enum(TypeSend), nullable=False)
    status = Column(Enum(Status), nullable=False)
    responseServer = Column(Text, default="No response")
    createdAt = Column(TIMESTAMP, server_default=func.current_timestamp())
    endIn = Column(TIMESTAMP, server_default=func.current_timestamp())



    