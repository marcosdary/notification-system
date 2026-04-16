from sqlalchemy import delete
from time import time

from app.core import LOGGER as logger
from app.config import SessionLocalSync as SessionSync
from app.constants import StatusWebhook
from app.models import WebhookModel
from app.exceptions import (
    NotFoundError,
    ForbiddenActionError,
    DatabaseUnknownError
)
from app.schemas.webhook_schema import (
    ReadWebhookSchema,
    CreateWebhookSchema,
    UpdateWebhookSchema,
    ListWebhookSchema
)


class WebhookRepository:
    def __init__(self):
        self.__table = "webhook"


    def create(self, schema: CreateWebhookSchema) -> ReadWebhookSchema:
        repository = "WebhookRepository.create"

        with SessionSync() as session:
            start = time()

            try:
                logger.info(
                    "Iniciando criação de webhook.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_CREATE_START",
                        "repository": repository,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                webhook = WebhookModel(**schema.model_dump())
                session.add(webhook)
                session.commit()

                execution = time() - start

                logger.info(
                    "Webhook criado com sucesso.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_CREATE_SUCCESS",
                        "repository": repository,
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                return ReadWebhookSchema.model_validate(webhook)

            except Exception as exc:
                session.rollback()

                logger.exception(
                    "Erro ao criar webhook.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_CREATE_ERROR",
                        "repository": repository,
                        "error": str(exc),
                        "type_error": exc.__class__.__name__,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )
                raise DatabaseUnknownError(f"(create) {str(exc)}")


    def select_by_id(self, idWebhook: str) -> ReadWebhookSchema:
        repository = "WebhookRepository.select_by_id"

        with SessionSync() as session:
            start = time()

            try:
                logger.info(
                    "Buscando webhook por ID.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_SELECT_BY_ID_START",
                        "repository": repository,
                        "idWebhook": idWebhook,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                webhook = session.query(WebhookModel).filter(
                    WebhookModel.idWebhook == idWebhook
                ).first()

                if not webhook:
                    raise NotFoundError("Webhook não encontrado.")

                execution = time() - start

                logger.info(
                    "Webhook encontrado com sucesso.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_SELECT_BY_ID_SUCCESS",
                        "repository": repository,
                        "idWebhook": idWebhook,
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                return ReadWebhookSchema.model_validate(webhook)

            except Exception as exc:
                logger.exception(
                    "Erro ao buscar webhook por ID.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_SELECT_BY_ID_ERROR",
                        "repository": repository,
                        "idWebhook": idWebhook,
                        "layer": "repository",
                        "error": str(exc),
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise DatabaseUnknownError(f"(select_by_id) {str(exc)}")


    def select_all(self) -> ListWebhookSchema:
        repository = "WebhookRepository.select_all"

        with SessionSync() as session:
            start = time()

            try:
                logger.info(
                    "Buscando todos os webhooks.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_SELECT_ALL_START",
                        "repository": repository,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                webhooks = session.query(WebhookModel).all()

                if not webhooks:
                    raise NotFoundError("Nenhum webhook encontrado.")

                execution = time() - start

                logger.info(
                    "Webhooks listados com sucesso.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_SELECT_ALL_SUCCESS",
                        "repository": repository,
                        "rows": len(webhooks),
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                return ListWebhookSchema(
                    info=[
                        ReadWebhookSchema.model_validate(row)
                        for row in webhooks
                    ]
                )

            except Exception as exc:
                logger.exception(
                    "Erro ao listar webhooks.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_SELECT_ALL_ERROR",
                        "repository": repository,
                        "error": str(exc),
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                        "layer": "repository",
                    }
                )
                raise DatabaseUnknownError(f"(select_all) {str(exc)}")


    def update(self, schema: UpdateWebhookSchema) -> None:
        repository = "WebhookRepository.update"

        with SessionSync() as session:
            start = time()

            try:
                logger.info(
                    "Iniciando atualização de webhook.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_UPDATE_START",
                        "repository": repository,
                        "idWebhook": schema.idWebhook,
                        "table": self.__table,
                        "layer": "repository",
                    }
                )

                webhook = session.query(WebhookModel).filter(
                    WebhookModel.idWebhook == schema.idWebhook
                ).first()

                if not webhook:
                    raise NotFoundError("Webhook não encontrado.")

                for key, value in schema.model_dump().items():
                    if value:
                        setattr(webhook, key, value)

                session.add(webhook)
                session.commit()

                execution = time() - start

                logger.info(
                    "Webhook atualizado com sucesso.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_UPDATE_SUCCESS",
                        "repository": repository,
                        "idWebhook": schema.idWebhook,
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

            except Exception as exc:
                session.rollback()

                logger.exception(
                    "Erro ao atualizar webhook.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_UPDATE_ERROR",
                        "repository": repository,
                        "idWebhook": schema.idWebhook,
                        "layer": "repository",
                        "error": str(exc),
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise DatabaseUnknownError(f"(update) {str(exc)}")


    # =========================
    # DELETE
    # =========================
    def delete(self, idWebhook: str) -> None:
        repository = "WebhookRepository.delete"

        with SessionSync() as session:
            start = time()

            try:
                logger.info(
                    "Iniciando deleção de webhook.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_DELETE_START",
                        "repository": repository,
                        "idWebhook": idWebhook,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                webhook = session.query(WebhookModel).filter(
                    WebhookModel.idWebhook == idWebhook
                ).first()

                if not webhook:
                    raise NotFoundError("Webhook não encontrado.")

                if webhook.status == StatusWebhook.PENDING:
                    raise ForbiddenActionError("Ação proibida enquanto status for PENDING.")

                session.delete(webhook)
                session.commit()

                execution = time() - start

                logger.info(
                    "Webhook deletado com sucesso.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_DELETE_SUCCESS",
                        "repository": repository,
                        "idWebhook": idWebhook,
                        "layer": "repository",
                        "execution_time": execution,
                        "table": self.__table,
                    }
                )

            except Exception as exc:
                session.rollback()

                logger.exception(
                    "Erro ao deletar webhook.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_DELETE_ERROR",
                        "repository": repository,
                        "idWebhook": idWebhook,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise DatabaseUnknownError(f"(delete) {str(exc)}")


    def delete_all(self) -> None:
        repository = "WebhookRepository.delete_all"

        with SessionSync() as session:
            start = time()

            try:
                logger.info(
                    "Iniciando deleção de todos os webhooks.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_DELETE_ALL_START",
                        "repository": repository,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

                session.execute(delete(WebhookModel))
                session.commit()

                execution = time() - start

                logger.info(
                    "Todos os webhooks foram deletados.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_DELETE_ALL_SUCCESS",
                        "repository": repository,
                        "execution_time": execution,
                        "layer": "repository",
                        "table": self.__table,
                    }
                )

            except Exception as exc:
                session.rollback()

                logger.exception(
                    "Erro ao deletar todos os webhooks.",
                    extra={
                        "event": "WEBHOOK_REPOSITORY_DELETE_ALL_ERROR",
                        "repository": repository,
                        "error": str(exc),
                        "layer": "repository",
                        "type_error": exc.__class__.__name__,
                        "table": self.__table,
                    }
                )
                raise DatabaseUnknownError(str(exc))