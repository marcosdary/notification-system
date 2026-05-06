from app.schemas import EmailSchema
from app.services import LoadTemplate, EmailService, file_to_base64
from app.core.constants import UPLOADS_DIR


email = EmailSchema.model_validate({
    "to": [
        {
            "name": "Marcos Wyliam",
            "email": "mw.oliveira.work@gmail.com",
        },
        {
            "name": "Marcos Wyliam",
            "email": "marcoswyliamking@gmail.com"
        }
    ],
    "subject": "Aviso importante",
    "template": "REGISTER",
    "variables": {
        "link": "https://www.google.com"
    }
})

load_template = LoadTemplate()

html = load_template.load(
    name=email.template.value,
    info=email.variables.model_dump()
)

email_service = EmailService()

recipients = list(map(lambda a: a.email, email.to))

path_file = UPLOADS_DIR / "file.epub"
base64 = file_to_base64(path_file)

email_service.send(
    recipients=recipients,   
    subject=email.subject,
    body=html
)




