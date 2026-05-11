from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.models import FileModel
from app.core.constants import StatusFile
from app.exceptions import NotFoundError


class FileRepository:
    def __init__(self, session: Session):
        self.session = session 
    
    def get_by_id(self, path: str) -> FileModel:
        query = select(FileModel).filter(FileModel.path == path)
        stmt = self.session.scalar(query)

        if not stmt:
            raise NotFoundError("Recurso solicitado não é encontrado.")
        
        return stmt
    
    def get_all(self) -> List[FileModel]:
        query = select(FileModel).filter(FileModel.status == StatusFile.used)
        stmt = self.session.scalars(query)

        if not stmt:
            raise NotFoundError("Recurso solicitado não é encontrado.")
        
        return stmt
    
   
    



