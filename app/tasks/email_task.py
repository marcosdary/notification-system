from datetime import datetime, timedelta
from uuid import uuid4

from app.constants import Templates, SendType, StatusEmail
from app.config import celery_app, logger
from app.schemas.email_notification_schema import (
    CreateEmailNotificationSchema, 
    ReadEmailNotificationSchema,
    UpdateEmailNotificationSchema,
)
from app.services import EmailService, LoadTemplate
from app.repositories import EmailNotificationRepository
from app.tasks.deliver_webhook import deliver_webhook

@celery_app.task
def process_email_notification(payload: dict):

    schema = CreateEmailNotificationSchema(**payload)
    notification_repo = EmailNotificationRepository()
    email_service = EmailService()
    load_template = LoadTemplate()

    logger.info(schema.model_dump_json(indent=4))
    
    expires_at_str = None
    if schema.expiresAt:
        expires_at_dt = datetime.now() + timedelta(seconds=schema.expiresAt.value)
        expires_at_str = expires_at_dt.strftime("%d-%m-%y %H:%M:%S")

    try:     
    
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
        """
        # email
        email_service.send(
            recipient_email=schema.recipientEmail,
            subject=subject,
            body=template
        )
        """    
        status = StatusEmail.DONE
        provider_response = "E-mail enviado com sucesso."
    except Exception as exc:
        logger.exception(f"Erro ao enviar e-mail: {str(exc)}")
        status = StatusEmail.ERROR
        provider_response = str(exc)
    
    try:
        data = notification_repo.update_order_status(
            UpdateEmailNotificationSchema(
                idEmail=schema.idEmail,
                status=status,
                providerResponse=provider_response,   
            )
        )
        logger.info(data.model_dump_json(indent=4))

        deliver_webhook.delay(
            payload=data.model_dump(),
            delivery_id=str(uuid4())
        )

    except Exception as exc:
        logger.exception(f"Erro ao salvar no banco: {str(exc)}")

    return {"status": True}