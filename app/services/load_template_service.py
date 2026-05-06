from jinja2 import FileSystemLoader, Environment

from app.core.constants import TEMPLATES_DIR
from app.core.constants import FileTemplate
class LoadTemplate:
    def __init__(self):
        self._env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def load(self, name: str, info: dict) -> str:
        file_template = FileTemplate.get_value(name)
        template = self._env.get_template(file_template.value)
        html = template.render(**info) 
        return html

