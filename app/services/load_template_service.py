from jinja2 import FileSystemLoader, Environment

from app.core import LOGGER as logger
from app.constants import TEMPLATES_DIR

class LoadTemplate:
    def __init__(self):
        self._env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def load(self, name_template: str, info: dict) -> str:
        logger.info(
            "Carregando o template para envio de notificação.",
            extra={
                "event": "LOAD_TEMPLATE_START",
                "services": "LoadTemplate",
                "layer": "services",
                "template": {
                    "name": name_template,
                    "info": info
                }, 
            }
        )
        template = self._env.get_template(name_template)
        html = template.render(**info) 
        return html
