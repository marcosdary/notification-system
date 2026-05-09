from fastapi import APIRouter, UploadFile, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timedelta
from uuid import uuid4

from app.core.storage import get_client_supabase
from app.core.config import settings, get_session
from app.schemas.file_schema import FileUploadSchema, FilesUploadSchema
from app.repositories import TemporaryFilesRepository

router = APIRouter()

@router.post("/uploadfile", status_code=status.HTTP_201_CREATED, response_model=FilesUploadSchema)
async def upload_file(files: List[UploadFile], session: AsyncSession = Depends(get_session)):
    upload_files = [] 

    temporary_files_repo = TemporaryFilesRepository(session)
    await temporary_files_repo.create()
    await session.commit()

    client_supabase = await get_client_supabase()
    storage = client_supabase.storage.from_(settings.BUCKET_FILES_PUBLIC)
    
    for file in files:
    
        *_, extension = file.filename.split('.')
        name = f"file_{uuid4()}.{extension}"
        
        upload_response = await (
            storage
            .upload(
                path=name,
                file=file.file.read()
            )
        )

        upload_files.append(upload_response.path)

    expires_in = settings.EXPIRES_IN_SIGNED_URL

    signed_urls_response = await storage.create_signed_urls(upload_files, expires_in=expires_in)

    return FilesUploadSchema.model_validate(
        [
            FileUploadSchema(
                expires_at=datetime.now() + timedelta(seconds=expires_in),
                error=row.get("error"),
                path=row.get("path"),
                signed_url=row.get("signedURL")
            )
            for row in signed_urls_response
        ]
    )