from typing import Optional, Any, Dict

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader(
        package_name="src.main", package_path="../resources/templates"
    ),
    autoescape=select_autoescape(["html"]),
)


def render_template(_filename: str, values: Optional[Dict[str, Any]] = None, **kwargs):
    """
    Renders template & returns text
    :param _filename: Name of template
    :param values: Values for template (optional)
    :param kwargs: Keyword-arguments for template (high-priority)

    """

    template = env.get_template(_filename)

    if values:
        rendered_template = template.render(values, **kwargs)
    else:
        rendered_template = template.render(**kwargs)

    return rendered_template
