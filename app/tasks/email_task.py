from datetime import datetime, timedelta

from app.core.constants import Templates, SendType, StatusEmail
from app.core.config import celery_app
from app.schemas.email_notification_schema import (
    EmailNotificationCreateSchema, 
    EmailNotificationUpdateSchema,
)
from app.services import EmailService, LoadTemplate
from app.repositories import EmailNotificationRepository

@celery_app.task
def process_email_notification(payload: dict):

    schema = EmailNotificationCreateSchema(**payload)
    notification_repo = EmailNotificationRepository()
    email_service = EmailService()
    load_template = LoadTemplate()
    
    try:     

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

        
        status = StatusEmail.DONE
        provider_response = "E-mail enviado com sucesso."
        
    except Exception as exc:
        status = StatusEmail.ERROR
        provider_response = str(exc)
    
    try:
        data = notification_repo.update(
            EmailNotificationUpdateSchema(
                idEmail=schema.idEmail,
                status=status,
                providerResponse=provider_response,   
            )
        )


    except Exception as exc:  
        pass
    
    return {"status": True}