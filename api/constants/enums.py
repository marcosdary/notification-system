from enum import Enum

class SendType(Enum):
    REGISTER = "REGISTER"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    TWO_FACTOR_AUTH = "TWO_FACTOR_AUTH"
    PASSWORD_RESET = "PASSWORD_RESET"

class Status(Enum):
    PENDING = "PENDING"
    DONE = "DONE"
    ERROR = "ERROR"
    REJECTED = "REJECTED"

class Templates(Enum):
    PASSWORD_CHANGE = "password_change.html"
    REGISTER = "register.html"
    PASSWORD_RESET = "password_reset.html"
    TWO_F_AUTH = "two_f_auth.html"

class ExpirationAt(Enum):
    TEN_MINUTES     = 10 * 60
    FIFTEEN_MINUTES = 15 * 60
    TWENTY_MINUTES  = 20 * 60
    ONE_HOUR        = 60 * 60

