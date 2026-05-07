from fastapi import APIRouter, UploadFile, status
import shutil
from typing import List
from uuid import uuid4

from app.core.constants import UPLOADS_DIR
from app.schemas.file_schema import FileUploadSchema

router = APIRouter()

@router.post("/uploadfile", status_code=status.HTTP_201_CREATED, response_model=FileUploadSchema)
async def upload_file(files: List[UploadFile]):
    response = [] 

    for file in files:
        *_, extension = file.filename.split('.')
        name = f"file_{uuid4()}.{extension}"
        path = UPLOADS_DIR / name
        
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        response.append(name)

    return FileUploadSchema(files=response)