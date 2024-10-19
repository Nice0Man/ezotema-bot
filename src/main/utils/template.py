from typing import Optional, Any, Dict

from jinja2 import Environment, PackageLoader, select_autoescape

ERROR_IMG_ID = "AgACAgIAAxkBAAIFTWcMB-5Vp-YBCjz0mQHVoOGUoxbsAAIt5jEbKlRgSO3hjcuJ9PEuAQADAgADeQADNgQ"

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


async def add_image_id(album_builder, image_ids):
    for i in range(len(image_ids)):
        media = image_ids.get(f"photo_{i + 1}")
        if not media:
            media = ERROR_IMG_ID
        album_builder.add_photo(media=media)
