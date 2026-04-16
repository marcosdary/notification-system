import logging
import sys
from colorlog import ColoredFormatter
import json_log_formatter

class AppJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        return {
            "timestamp": record.created,
            "logger": record.name,
            "event": extra.get("event", "UNDEFINED_EVENT"),
            "message": message,
            **extra
        }
    
class SimpleFormatter(ColoredFormatter):
    def __init__(self):
        super().__init__(
            "%(log_color)s[%(levelname)s]%(reset)s %(blue)s%(name)s%(reset)s: %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        )

def setup_logger():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # Handler para terminal (legível)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(SimpleFormatter())
    
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(AppJSONFormatter())

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


LOGGER = setup_logger()