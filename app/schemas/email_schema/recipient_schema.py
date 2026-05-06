from pydantic import BaseModel, ConfigDict, EmailStr


class RecipientSchema(BaseModel):
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

