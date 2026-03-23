from datetime import datetime, timedelta, timezone
from celery.utils.log import get_task_logger

from api.constants import Templates, SendType, Status
from api.config import celery_app
from api.schemas.email_notification_schemas import CreateEmailNotificationSchema
from api.services import EmailService, LoadTemplate
from api.repositories import EmailNotificationRepository

logger = get_task_logger(__name__)

@celery_app.task
def process_email_notification(data: dict):

    schema = CreateEmailNotificationSchema(**data)

    notification_repo = EmailNotificationRepository()
    email_service = EmailService()
    load_template = LoadTemplate()

    logger.info(schema.model_dump_json(indent=4))
    
    expires_at_str = None
    if schema.expiresAt:
        expires_at_dt = datetime.now(timezone.utc) + timedelta(seconds=schema.expiresAt.value)
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
            
        status = Status.DONE
        provider_response = "E-mail enviado com sucesso."
    except Exception as exc:
        logger.exception("Erro ao processar email")
        status = Status.ERROR
        provider_response = str(exc)
    
    processed_at = datetime.now(timezone.utc)

    try:
        notification_repo.update_order_status(
            idEmail=schema.idEmail,
            status=status,
            providerResponse=provider_response,
            processedAt=processed_at
        )
    except Exception as exc:
        logger.exception("Erro ao salvar no banco")

    return {"status": status.value}