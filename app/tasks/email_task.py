from datetime import datetime, timedelta
from uuid import uuid4
from time import time

from app.constants import Templates, SendType, StatusEmail
from app.core import LOGGER as logger
from app.config import celery_app
from app.schemas.email_notification_schema import (
    CreateEmailNotificationSchema, 
    UpdateEmailNotificationSchema,
)
from app.services import EmailService, LoadTemplate
from app.repositories import EmailNotificationRepository
from app.tasks.deliver_webhook import deliver_webhook

@celery_app.task
def process_email_notification(payload: dict):
    task = "task.process_email_notification"
    logger.info(
        "Iniciando a tarefa de envia a notificação para e-mail",
        extra={
            "event": "PROCESS_EMAIL_NOTIFICATION_START",
            "task": task,
            "layer": "task"
        }
    )
    start = time()

    schema = CreateEmailNotificationSchema(**payload)
    notification_repo = EmailNotificationRepository()
    email_service = EmailService()
    load_template = LoadTemplate()
    
    logger.debug(
        schema.model_dump_json(indent=4),
        extra={
            "event": "PROCCESS_EMAIL_NOTIFICATION_DEBUG",
            "task": task,
            "layer": "task"
        }
    )
    try:     
        logger.debug(
            "O processo de construção e-mail está sendo feito",
            extra={
                "event": "EMAIL_NOTIFICATION_SENDING_DEBUG_START",
                "task": task,
                "layer": "task"
            }
        )
        start_email_sending_time = time()

        expires_at_str = None
        if schema.expiresAt:
            expires_at_dt = datetime.now() + timedelta(seconds=schema.expiresAt.value)
            expires_at_str = expires_at_dt.strftime("%d-%m-%y %H:%M:%S")
    
        # template
        templates = {
            SendType.REGISTER: Templates.REGISTER,
            SendType.PASSWORD_CHANGE: Templates.PASSWORD_CHANGE,
            SendType.PASSWORD_RESET: Templates.PASSWORD_RESET,
            SendType.TWO_FACTOR_AUTH: Templates.TWO_F_AUTH,
        }

        template_enum = templates.get(schema.sendType)
        if not template_enum:
            raise ValueError(f"SendType inválido: {schema.sendType}")


        template = load_template.load(
            name_template=template_enum.value, 
            info={
                "expiresAt": expires_at_str,
                "token": schema.token,
                "code": schema.code,
                "actionLink": schema.actionLink
            }
        )
        
        # subject
        subjects = {
            SendType.REGISTER: "Confirmação de Cadastro",
            SendType.PASSWORD_CHANGE: "Confirmação de Alteração de Senha",
            SendType.PASSWORD_RESET: "Redefinição de Senha",
            SendType.TWO_FACTOR_AUTH: "Verificação de 2 fatores",
        }

        subject = subjects.get(schema.sendType, "Notificação")

        
        # email
        email_service.send(
            recipient_email=schema.recipientEmail,
            subject=subject,
            body=template
        )
    
        email_sending_time = time() - start_email_sending_time
        
        status = StatusEmail.DONE
        provider_response = "E-mail enviado com sucesso."
        
        logger.info(
            "O envio de e-mail concluída com sucesso.",
            extra={
                "event": "EMAIL_NOTIFICATION_SENDING_SUCCESS",
                "task": task,
                "layer": "task",
                "email_sending_time": email_sending_time,
                "template": template_enum.value
            }
        )  
        
    except Exception as exc:
        logger.exception(
            "Erro ao envia o e-mail",
            extra={
                "event": "EMAIL_NOTIFICATION_SENDING_ERROR",
                "task": task,
                "error": str(exc),
                "layer": "task",
                "type_error": exc.__class__.__name__,
            }
        )
        status = StatusEmail.ERROR
        provider_response = str(exc)
    
    try:
        data = notification_repo.update(
            UpdateEmailNotificationSchema(
                idEmail=schema.idEmail,
                status=status,
                providerResponse=provider_response,   
            )
        )

        deliver_webhook.delay(
            payload=data.model_dump(),
            delivery_id=str(uuid4())
        )
        logger.info(
            "Atualizada com sucesso as informações da notificação de e-mail.",
            extra={
                "event": "EMAIL_NOTIFICATION_UPDATE_SUCCESS",
                "task": task,
                "layer": "task",
                "idEmail": data.idEmail,
            }
        )  

    except Exception as exc:
        logger.exception(
            "Erro ao atualizar as informações da notificação",
            extra={
                "event": "EMAIL_NOTIFICATION_UPDATE_ERROR",
                "task": task,
                "error": str(exc),
                "layer": "task",
                "type_error": exc.__class__.__name__,
            }
        )
    
    execution = time() - start

    logger.info(
        "A tarefa de envia a notificação para e-mail concluída com sucesso",
        extra={
            "event": "PROCESS_EMAIL_NOTIFICATION_SUCCESS",
            "mutation": task,
            "layer": "task",
            "execution": execution
        }
    ) 
    
    return {"status": True}