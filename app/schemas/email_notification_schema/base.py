from pydantic import BaseModel, ConfigDict


class EmailNotificationBaseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

  