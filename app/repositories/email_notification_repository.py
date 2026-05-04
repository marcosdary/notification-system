from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, and_, func
from datetime import datetime

from app.core.config import SessionLocalAsync as SessionAsync, SessionLocalSync as SessionSync
from app.core.constants import StatusEmail, SendType
from app.exceptions import (
    EntityValidationError,
    UnknownError,
    NotFoundError,
    ForbiddenActionError
)
from app.schemas.email_notification_schema import (
    EmailNotificationCreateSchema,
    EmailNotificationReadSchema,
    ListEmailNotificationSchema,
    EmailNotificationUpdateSchema,
)
from app.schemas import PaginationSchema, DateRangeSchema
from app.models import EmailNotificationsModel


class EmailNotificationRepository:


    def __init__(self):
        self.__table = "email_notification"

    def _build_filters(
        self,
        date_range: DateRangeSchema | None,
        status_email: StatusEmail | None,
        send_type: SendType | None,
        date: datetime | None
    ) -> list:
        filters = []
                
        if date_range:
            filters.append(
                EmailNotificationsModel.createdAt.between(
                date_range.startDate,
                date_range.endDate
            )
        )

        if status_email:
            filters.append(EmailNotificationsModel.status == status_email)
                
        if send_type:
            filters.append(EmailNotificationsModel.sendType == send_type)

        if date:
            filters.append(func.date(EmailNotificationsModel.createdAt) == date)

        return filters

    async def _count(self, session, filters: list) -> int:
        count_query = select(func.count()).select_from(EmailNotificationsModel)
        if filters:
            count_query = count_query.where(and_(*filters))
        return await session.scalar(count_query)
    
    def _build_query(self, filters: list, pagination: PaginationSchema):
        query = select(EmailNotificationsModel)

        if filters:
            query = query.where(and_(*filters))

        if filters:
            query = query.where(and_(*filters))

        if not pagination.all_:
            offset = (pagination.page - 1) * pagination.limit
            query = query.offset(offset).limit(pagination.limit)

        return query.order_by(EmailNotificationsModel.createdAt.desc())

    async def create(self, schema: EmailNotificationCreateSchema) -> EmailNotificationReadSchema:


        async with SessionAsync() as session:
           

            try:
               
                notif = EmailNotificationsModel(**schema.model_dump())
                session.add(notif)
                await session.commit()
                return EmailNotificationReadSchema.model_validate(notif)

            except IntegrityError as exc:
                await session.rollback()

                raise EntityValidationError("Erro de integridade nos dados.")

            except Exception as exc:
                await session.rollback()

                raise UnknownError("Erro desconhecido ao salvar dados.")

    async def select_by_id(self, idEmail: str) -> EmailNotificationReadSchema:

        async with SessionAsync() as session:
        

            try:

                stmt = await session.execute(
                    select(EmailNotificationsModel).where(
                        EmailNotificationsModel.idEmail == idEmail
                    )
                )

                notif = stmt.scalars().first()

                if not notif:
                    raise NotFoundError("Notificação não encontrada.")

               

                return EmailNotificationReadSchema.model_validate(notif)

            except Exception as exc:
        
                raise

    async def select_filter_all(
        self, 
        pagination: PaginationSchema, 
        date_range: DateRangeSchema = None,
        status_email: StatusEmail = None, 
        send_type: SendType = None,
        date: datetime = None
    ) -> ListEmailNotificationSchema:

        async with SessionAsync() as session:
            try:
                
                filters = self._build_filters(date_range, status_email, send_type, date)          

                total = await self._count(session, filters)
                
                query = self._build_query(filters, pagination)

                stmt = await session.execute(query)
                records = stmt.scalars().all()

                if not records:
                    raise NotFoundError("Nenhuma notificação encontrada.")
                

                return ListEmailNotificationSchema(
                        items=[
                            EmailNotificationReadSchema.model_validate(row)
                            for row in records
                        ],
                        limit=pagination.limit,
                        page=pagination.page,
                        total=total,
                        hasNextPage=(pagination.page * pagination.limit) < total
                )
            
            except Exception as exc:
                
                raise


    def update(self, schema: EmailNotificationUpdateSchema) -> EmailNotificationReadSchema:
       

        with SessionSync() as session:

            try:
                

                notif = session.query(EmailNotificationsModel).filter(
                    EmailNotificationsModel.idEmail == schema.idEmail
                ).first()

                if not notif:
                    raise NotFoundError("Notificação não encontrada.")

                for key, value in schema.model_dump().items():
                    setattr(notif, key, value)

                session.commit()

                return EmailNotificationReadSchema.model_validate(notif)

            except Exception as exc:
                session.rollback()

                raise


    async def delete(self, idEmail: str) -> None:

        async with SessionAsync() as session:
            

            try:
        

                stmt = await session.execute(
                    select(EmailNotificationsModel).where(
                        EmailNotificationsModel.idEmail == idEmail
                    )
                )

                notif = stmt.scalars().first()

                if not notif:
                    raise NotFoundError("Notificação não encontrada.")

                if notif.status == StatusEmail.PENDING:
                    raise ForbiddenActionError("Ação proibida para status PENDING.")

                await session.delete(notif)
                await session.commit()
               

            except Exception as exc:
                await session.rollback()

                raise


    async def delete_all(self) -> None:

        async with SessionAsync() as session:

            try:

                await session.execute(delete(EmailNotificationsModel))
                await session.commit()


            except Exception as exc:
                await session.rollback()

                raise