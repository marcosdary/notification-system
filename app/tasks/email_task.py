from os import remove

from app.celery import celery_app
from app.schemas.email_schema import EmailSchema, AttachmentSchema
from app.services import EmailService, LoadTemplate, file_to_base64
from app.core.constants import UPLOADS_DIR

@celery_app.task(pydantic=True)
def process_send_email(schema: EmailSchema):

    email_service = EmailService()
    load_template = LoadTemplate()
    
    recipients = list(map(lambda a: a.email, schema.to))
    attachments = list()
    
    for attachment in schema.attachments:
        if not attachment.path:
            path = UPLOADS_DIR / attachment.filename

            if not path.exists():
                continue

            base64 = file_to_base64(path)
            
            attachments.append(
                AttachmentSchema(
                    filename=attachment.filename, 
                    content=base64
                ).model_dump(exclude_none=True)
            )
            path.unlink(missing_ok=True)
            continue
        
        attachments.append(attachment.model_dump(exclude_none=True))

    
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
     
    
