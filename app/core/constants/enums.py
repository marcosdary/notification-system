from enum import Enum

class FileTemplate(Enum):
    REGISTER        = "register.html"
    PASSWORD_CHANGE = "password_change.html"
    TWO_FACTOR_AUTH = "two_factor_auth.html"
    PASSWORD_RESET  = "password_reset.html"

    @classmethod
    def get_value(cls, name: str):
        member = cls.__members__.get(name)
        if not member:
            raise KeyError("Membro incorreto")
        return member


class Status(Enum):
    sent        = "sent"
    # Ocorre sempre que a solicitação da API foi bem-sucedida. Resend vai tentar 
    # entregar a mensagem para o servidor de e-mail do destinatário.
    bounced     = "bounced"
    # Ocorre sempre que o servidor de correio do destinatário rejeitou permanentemente 
    # o e-mail.
    complained  = "complained"
    # Ocorre sempre que o e-mail foi entregue com sucesso, mas o destinatário marcou 
    # como spam.
    delivered   = "delivered"
    # Ocorre sempre que Reenviar entregue com sucesso o e-mail para o servidor de 
    # correio do destinatário.
    delivery_delayed = "delivery_delayed" 
    # Ocorre sempre que o e-mail não pôde ser entregue devido a um 
    # temporário questão. Os atrasos de entrega podem ocorrer, por exemplo, 
    # quando o destinatário caixa de entrada está cheia, ou quando o servidor de e-mail 
    # receptor experimenta um transitório questão.
    failed     = "failed"
    # Ocorre sempre que o e-mail não foi enviado devido a um erro. Este evento é acionado 
    # quando há problemas como destinatários inválidos, chave de API problemas, problemas 
    # de verificação de domínio, limites de cota de e-mail ou outro envio fracassos.
    received   = "received"  
    # Ocorre sempre que o Resend recebe com sucesso um e-mail.   

class Template(Enum):
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    REGISTER        = "REGISTER"
    PASSWORD_RESET  = "PASSWORD_RESET"
    TWO_FACTOR_AUTH = "TWO_FACTOR_AUTH"

class StatusWebhook(Enum):
    PENDING     = "PENDING"
    SUCCESS    = "SUCCESS"
    FAILED      = "FAILED"
    RETRYING    = "RETRYING"
    DEAD_LETTE  = "DEAD_LETTER"
  
class ExpirationTime(Enum):
    TEN_MINUTES     = 10 * 60
    FIFTEEN_MINUTES = 15 * 60
    TWENTY_MINUTES  = 20 * 60
    ONE_HOUR        = 60 * 60

