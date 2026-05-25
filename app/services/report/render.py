from jinja2 import Environment, FileSystemLoader

from app.services.report.constants import TEMPLATE_DIR


def render_report_html(context: dict) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=True)
    template = env.get_template("evaluation_report.html")
    return template.render(**context)
