from pydantic import BaseModel, ConfigDict, field_serializer
from enum import Enum

from app.constants import StatusWebhook

class BaseWebhookSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

 