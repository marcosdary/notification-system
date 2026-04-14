import logging
import sys
import json_log_formatter

class AppJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        return {
            "timestamp": record.created,
            "level": record.levelname.lower(),
            "logger": record.name,
            "service": "email-service",
            "event": extra.get("event", "UNDEFINED_EVENT"),
            "message": message,
            "trace_id": extra.get("trace_id"),
            "mutation": None,
            "layer": None,
            **extra
        }

def setup_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(AppJSONFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)

    return logging.getLogger("app")


LOGGER = setup_logger()