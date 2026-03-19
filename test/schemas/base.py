from pydantic import BaseModel, field_validator, ConfigDict
import re 

class BaseSchema(BaseModel):
    to_email: str

    @field_validator("to_email", mode="after")
    def validate_email(cls, value: str) -> str:
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, value) is None:
            raise Exception(
                "Campo e-mail inválido. Faça corretamente."
            )
        return value

    model_config = ConfigDict(from_attributes=True)