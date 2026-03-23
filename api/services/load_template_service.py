from jinja2 import FileSystemLoader, Environment

from api.constants import TEMPLATES_DIR

class LoadTemplate:
    def __init__(self):
        self._env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def load(self, name_template: str, info: dict) -> str:
        template = self._env.get_template(name_template)
        html = template.render(**info) 
        return html
