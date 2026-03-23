import resend

from api.config import settings

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
        try:
            resend.api_key = self._api_key_resend
            
            params: resend.Emails.SendParams = {
                "from": f"HorizonTecnology <{self._sender}>",
                "to": [recipient_email],
                "subject": subject,
                "html": body, 
            } 
            email: resend.Emails.SendResponse = resend.Emails.send(params)
            return email
        except Exception as exc:
            raise Exception(f"Erro externo do servidor: {str(exc)}")
