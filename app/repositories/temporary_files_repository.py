from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from datetime import datetime, timedelta

from app.models import TemporaryFilesModel
from app.core.config import settings
from app.exceptions import NotFoundError

class TemporaryFilesRepository:
    def __init__(self, session: Session | AsyncSession):
        self.session = session 

    async def create(self) -> None: 
        temporary_file = TemporaryFilesModel()
        temporary_file.expires_at = datetime.now() + timedelta(seconds=settings.EXPIRES_IN_FILE)
        self.session.add(temporary_file)
        return 
    
    def get_by_id(self, id_file: str) -> TemporaryFilesModel:
        query = select(TemporaryFilesModel).filter(TemporaryFilesModel.id_file == id_file)
        stmt = self.session.scalar(query)

        if not stmt:
            raise NotFoundError("Recurso solicitado não é encontrado.")
        
        return stmt
    
    def get_all(self) -> List[TemporaryFilesModel]:
        query = select(TemporaryFilesModel)
        stmt = self.session.scalars(query)

        if not stmt:
            raise NotFoundError("Recurso solicitado não é encontrado.")
        
        return stmt
    
    def remove(self) -> None:
        delete(TemporaryFilesModel).filter(TemporaryFilesModel.expires_at >= datetime.now())
        return 
    



