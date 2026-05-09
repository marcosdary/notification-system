from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from app.models import EmailModel
from app.schemas.email_schema import EmailTaskSchema
from app.exceptions import NotFoundError

class EmailRepository:
    def __init__(self, session: Session):
        self.session = session 

    def create(self, schema: EmailTaskSchema) -> None: 
        email = EmailModel(**schema.model_dump())
        self.session.add(email)
        return 
    
    def update(self, schema: EmailTaskSchema) -> EmailModel:
        query = select(EmailModel).filter(EmailModel.id_email == schema.id_email)
        stmt = self.session.scalar(query)

        if not stmt:
            raise NotFoundError("Recurso solicitado não é encontrado.")

        for key, value in schema.model_dump().items():
            if value:
                setattr(stmt, key, value)

        return stmt
    
    def get_by_id(self, id_email: str) -> EmailModel:
        query = select(EmailModel).filter(EmailModel.id_email == id_email)
        stmt = self.session.scalar(query)

        if not stmt:
            raise NotFoundError("Recurso solicitado não é encontrado.")
        
        return stmt
    
    def remove(self, id_email: str) -> None:
        query = select(EmailModel).filter(EmailModel.id_email == id_email)
        stmt = self.session.scalar(query)

        if not stmt:
            raise NotFoundError("Recurso solicitado não é encontrado.")
        
        self.session.delete(stmt)
        return 
    



