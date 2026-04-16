import resend
from time import time

from app.config import settings
from app.core import LOGGER as logger

class EmailService:

    def __init__(self) -> None:
        
        self._api_key_resend = settings.API_KEY_RESEND
        self._sender = settings.SENDER

    def send(self, recipient_email: str, subject: str, body: str) -> dict:
        """Envia um e-mail com assunto e corpo em HTML.

        Configura a chave de API, define remetente, destinatário, assunto
        e conteúdo HTML, e realiza o envio através da API Resend.

        Args:
            subject (str): Assunto do e-mail.
            body (str): Corpo do e-mail em HTML.

        Returns:
            dict: Resposta da API Resend contendo informações do envio.

        Raises:
            Exception: Se ocorrer algum erro externo durante o envio.
        """
        service = "EmailService.send"
        logger.info(
            "Iniciando o ferramente de e-mail (Resend)",
            extra={
                "event": "EMAIL_SERVICE_START",
                "services": service,
                "layer": "services"
            }
        )
        try:
            start = time()
            resend.api_key = self._api_key_resend
            
            params: resend.Emails.SendParams = {
                "from": f"HorizonTecnology <{self._sender}>",
                "to": [recipient_email],
                "subject": subject,
                "html": body, 
            } 
            email: resend.Emails.SendResponse = resend.Emails.send(params)

            execution = time() - start

            logger.info(
                "Concluir com sucesso a ferramente de e-mail (Resend)",
                extra={
                    "event": "EMAIL_SERVICE_SUCCESS",
                    "services": service,
                    "layer": "services",
                    "execution": execution
                }
            )

            return email
        except Exception as exc:
            logger.exception(
                "Falha na criação do e-mail",
                extra={
                    "event": "EMAIL_NOTIFICATION_CREATE_ERROR",
                    "services": service,
                    "layer": "services",
                    "error": str(exc),
                    "type_error": exc.__class__.__name__,
                }
            )
            raise Exception(f"Erro externo do servidor: {str(exc)}")
