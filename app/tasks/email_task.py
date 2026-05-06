from app.celery import celery_app
from app.schemas.email_schema import EmailSchema
from app.services import EmailService, LoadTemplate

@celery_app.task(pydantic=True)
def process_send_email(schema: EmailSchema):

    email_service = EmailService()
    load_template = LoadTemplate()
    
    recipients = list(map(lambda a: a.email, schema.to))
    attachments = list(map(lambda b: b.model_dump(exclude_none=True), schema.attachments))
    body = load_template.load(
        name=schema.template.value,
        info=schema.variables.model_dump(mode="json")
    )
                
    email_service.send(
        recipients=recipients,   
        subject=schema.subject,
        body=body,
        attachments=attachments
    )
    return 
     
    
