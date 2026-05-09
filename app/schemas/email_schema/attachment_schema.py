from pydantic import BaseModel

class AttachmentSchema(BaseModel):
    path: str 
    filename: str



