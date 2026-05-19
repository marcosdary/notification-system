from fastapi import APIRouter, UploadFile, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from typing import List
from uuid import uuid4
from storage3.exceptions import StorageApiError
from json import loads

from app.core.storage import get_client_supabase
from app.core.config import settings, get_session
from app.models import FileModel
from app.exceptions import NotFoundFile
from app.schemas.file_schema import FilesReadSchema, BaseFileSchema


router = APIRouter(tags=["file"])

@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=FilesReadSchema)
async def upload_file(files: List[UploadFile], session: AsyncSession = Depends(get_session)):
    try:
        upload_files = [] 
        values = []

        expires_in = settings.EXPIRES_IN_SIGNED_URL
        
        client_supabase = await get_client_supabase()

        storage = client_supabase.storage.from_(settings.BUCKET_FILES_PUBLIC)
        
        for file in files:
        
            *_, extension = file.filename.split('.')
            name = f"file_{uuid4()}.{extension}"
            
            values.append(BaseFileSchema(path=name).model_dump())

            upload_response = await (
                storage
                .upload(
                    path=name,
                    file=file.file.read()
                )
            )

            upload_files.append(upload_response.path)
            
        signed_urls_response = await storage.create_signed_urls(upload_files, expires_in=expires_in)
        
        await session.execute(
            insert(FileModel),
            values
        )
        await session.commit()
        return FilesReadSchema.model_validate(signed_urls_response)
    
    except Exception as exc:
        raise HTTPException(detail=f"Erro desconhecido: {str(exc)}")

@router.get("/download/{filename}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def download(filename: str):
    try:
        expires_in = settings.EXPIRES_IN_SIGNED_URL

        client_supabase = await get_client_supabase()
        storage = client_supabase.storage.from_(settings.BUCKET_FILES_PUBLIC)
        signed_upload_url = await storage.create_signed_url(
            filename,
            expires_in=expires_in,
            options={
                "download": True
            }
        )

        return RedirectResponse(
            url=signed_upload_url.get("signedURL"),
            headers={
                "Cache-Control": "no-store"
            }
        )
    except StorageApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )
    
    except Exception as exc:
        raise HTTPException(
            detail=f"Erro interno", 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
