from pydantic import BaseModel, ConfigDict

class VariablesSchema(BaseModel):
    link: str | None = None
    code: str | None = None
    expires_at: int | None = 15 

    model_config = ConfigDict(from_attributes=True)

    