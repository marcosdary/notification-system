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


class StatusEmail(Enum):
    PENDING     = "PENDING"
    STARTED     = "STARTED"
    SUCCESS     = "SUCCESS"
    FAILURE     = "FAILURE"
    REJECTED    = "REJECTED"
    REVOKED     = "REVOKED"

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

