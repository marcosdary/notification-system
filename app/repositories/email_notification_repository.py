from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from typing import List


from app.core.constants import StatusEmail
from app.exceptions import (
    EntityValidationError,
    UnknownError,
    NotFoundError,
    ForbiddenActionError
)
from app.schemas.email_notification_schema import (
    EmailNotificationCreateSchema,
    EmailNotificationUpdateSchema,
    EmailNotificationFilterBySchema
)
from app.schemas import PaginationSchema
from app.models import EmailNotificationsModel


class EmailNotificationRepository:


    def __init__(self, session: AsyncSession):
        self.session = session

    def _build_filters(
        self,
        filter_by: EmailNotificationFilterBySchema
    ) -> list:
        filters = []
                
        if filter_by.status:
            filters.append(EmailNotificationsModel.status == filter_by.status)
                
        if filter_by.sendType:
            filters.append(EmailNotificationsModel.sendType == filter_by.sendType)

        return filters


    def _build_query(self, filters: list, pagination: PaginationSchema):
        query = select(EmailNotificationsModel)

        if filters:
            query = query.where(and_(*filters))

        if not pagination.all_:
            offset = (pagination.page - 1) * pagination.limit
            query = query.offset(offset).limit(pagination.limit)

        return query.order_by(EmailNotificationsModel.createdAt.desc())

    async def create(self, schema: EmailNotificationCreateSchema) -> EmailNotificationsModel:
        try:
               
            notif = EmailNotificationsModel(**schema.model_dump())
            self.session.add(notif)
            return notif

        except IntegrityError as exc:
            raise EntityValidationError("Erro de integridade nos dados.")

        except Exception as exc:
            raise UnknownError("Erro desconhecido ao salvar dados.")

    async def select_by_id(self, idEmail: str) -> EmailNotificationsModel:
        notif = await self.session.scalar(
            select(EmailNotificationsModel).where(
                EmailNotificationsModel.idEmail == idEmail
            )
        )

        if not notif:
            raise NotFoundError("Notificação não encontrada.")

        return notif

    async def select_filter_all(
        self, 
        pagination: PaginationSchema, 
        filter_by: EmailNotificationFilterBySchema = None
    ) -> List[EmailNotificationsModel]:
        filters = []

        if filter_by:
            filters = self._build_filters(filter_by)          
                
        query = self._build_query(filters, pagination)

        records = await self.session.scalars(query)

        if not records:
            raise NotFoundError("Nenhuma notificação encontrada.")
                
        return records.all()
            
        
    def update(self, schema: EmailNotificationUpdateSchema) -> EmailNotificationsModel:
        notif = self.session.query(EmailNotificationsModel).filter(
            EmailNotificationsModel.idEmail == schema.idEmail
        ).first()

        if not notif:
            raise NotFoundError("Notificação não encontrada.")

        for key, value in schema.model_dump().items():
            setattr(notif, key, value)

        return notif


    async def delete(self, idEmail: str) -> None:  
        notif = await self.session.scalar(
            select(EmailNotificationsModel).where(
                EmailNotificationsModel.idEmail == idEmail
            )
        )

        if not notif:
            raise NotFoundError("Notificação não encontrada.")

        if notif.status == StatusEmail.PENDING:
            raise ForbiddenActionError("Ação proibida para status PENDING.")

        await self.session.delete(notif)
              


    async def delete_all(self) -> None:
        await self.session.execute(delete(EmailNotificationsModel))
              


           