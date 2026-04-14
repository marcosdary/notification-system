from enum import Enum
from pydantic import BaseModel, ConfigDict


class BaseEmailNotificationSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

  