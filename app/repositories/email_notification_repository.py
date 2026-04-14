from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete

from datetime import datetime

from app.config import SessionLocalAsync as SessionAsync, SessionLocalSync as SessionSync
from app.constants import StatusEmail
from app.exceptions import EntityValidationError, UnknownError, NotFoundError, ForbiddenActionError
from app.schemas.email_notification_schema import (
    CreateEmailNotificationSchema,
    ReadEmailNotificationSchema,
    ListEmailNotificationSchema,
    UpdateEmailNotificationSchema,
)
from app.models import EmailNotificationsModel


class EmailNotificationRepository:

    async def create(self, schema: CreateEmailNotificationSchema) -> ReadEmailNotificationSchema:
        async with SessionAsync() as session:
            try:
                notif = EmailNotificationsModel(**schema.model_dump())

                session.add(notif)
                await session.commit()        
                return ReadEmailNotificationSchema.model_validate(notif)
            
            except IntegrityError as exc:
                await session.rollback()
                raise EntityValidationError(f"Erro de integridade: {str(exc)}")
            
            except Exception as exc:
                await session.rollback()
                raise UnknownError(f"Erro desconhecido: {str(exc)}")

    async def select_by_id(self, idEmail: str) -> ReadEmailNotificationSchema:
        async with SessionAsync() as session:
            try:
                stmt = await session.execute(
                    select(EmailNotificationsModel).where(EmailNotificationsModel.idEmail == idEmail)
                )
                notif = stmt.scalars().first()
                if not notif:
                    raise NotFoundError("Nenhuma notificação por e-mail encontrada.")
                
                return ReadEmailNotificationSchema.model_validate(notif)

            except Exception as exc:
                raise exc

    async def select_all(self, page: int = 1, limit: int = 5) -> ListEmailNotificationSchema:
        async with SessionAsync() as session:
            try:
                offset = (page - 1) * limit
                stmt = await session.execute(
                    select(EmailNotificationsModel).offset(offset).limit(limit).order_by(EmailNotificationsModel.createdAt)
                )
                notifs = stmt.scalars().all()

                if not notifs:
                    raise NotFoundError("Nenhuma notificações por e-mail encontrada.")
                
                return ListEmailNotificationSchema(
                    notifications=[
                        ReadEmailNotificationSchema.model_validate(row)
                        for row in notifs
                    ]
                )

            except Exception as exc:
                raise exc

    def update_order_status(self, schema: UpdateEmailNotificationSchema) -> ReadEmailNotificationSchema:
        with SessionSync() as session:
            try:
                notif = session.query(EmailNotificationsModel).filter(EmailNotificationsModel.idEmail == schema.idEmail).first()
             
                if not notif:
                    raise NotFoundError("Não foi encontrada a notificação. Ocorreu um erro.")
            
                for key, value in schema.model_dump().items():
                    setattr(notif, key, value)
                
                session.commit()
                return ReadEmailNotificationSchema.model_validate(notif)

            except Exception as exc:
                session.rollback()
                raise 
            
    async def delete(self, idEmail: str) -> None:
        async with SessionAsync() as session:
            try:
                stmt = await session.execute(
                    select(EmailNotificationsModel).where(EmailNotificationsModel.idEmail == idEmail)
                )
                notif = stmt.scalars().first()

                if not notif:
                    raise NotFoundError("Nenhuma notificação encontrada.")
                
                if notif.status == StatusEmail.PENDING:
                    raise ForbiddenActionError("Ação proibida até que o status seja mudado.")
            
                await session.delete(notif)
                await session.commit()

            except Exception as exc:
                await session.rollback()
                raise 

    async def delete_all(self) -> None:
        async with SessionAsync() as session:
            try:
                await session.execute(
                    delete(EmailNotificationsModel)
                )
                await session.commit()

            except Exception as exc:
                await session.rollback()
                raise exc


            
        