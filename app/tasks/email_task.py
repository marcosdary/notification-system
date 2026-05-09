from uuid import uuid4

from app.celery import celery_app
from app.schemas.email_schema import EmailSchema, EmailTaskSchema
from app.services import EmailService, LoadTemplate
from app.core.config.database import SessionLocalSync as Session
from app.core.constants import Status
from app.repositories import EmailRepository

@celery_app.task(pydantic=True)
def process_send_email(schema: EmailSchema):

    email_service = EmailService()
    load_template = LoadTemplate()
    
    recipients = list(map(lambda a: a.email, schema.to))
    attachments = schema.attachments

    body = load_template.load(
        name=schema.template.value,
        info=schema.variables.model_dump(mode="json")
    )

    id_email = str(uuid4())
    message = "E-mail enviado com sucesso."

    try:        
        response: dict = email_service.send(
            recipients=recipients,   
            subject=schema.subject,
            body=body,
            attachments=attachments.model_dump() if attachments else None
        )
        id_email = response.get("id")
    except Exception as exc:
        message = str(exc)

    try:
        with Session() as session:
            email_repo = EmailRepository(session)
            email_repo.create(EmailTaskSchema(
                id_email=id_email,
                status=Status.sent,
                message=message
            ))
            session.commit()

    except Exception as exc:
        print(f"Erro na criação de salvar: {str(exc)}")

    return 
     
    
