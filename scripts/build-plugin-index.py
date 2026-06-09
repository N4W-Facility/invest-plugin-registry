import json
import logging
import re
from os import path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils import PLUGIN_TYPES


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
METADATA_PATH = path.join(path.dirname(__file__), '../html/metadata.json')
JINJA_TEMPLATE_DIR = path.join(path.dirname(__file__), '../source/jinja')
OUTPATH = path.join(path.dirname(__file__), '../source/plugins/plugins_index.html')


def load_plugin_json():
    with open(METADATA_PATH, 'r') as fin:
        plugins = json.load(fin)
        return plugins['data']


def sort_plugins(plugins: dict, sort_key: str = 'plugin_name') -> list[dict]:
    """Sort plugin data by the provided ``sort_key``.

    Args:
        plugins (dict): metadata for all plugins, indexed by the ``project_name``.
        sort_key (str): key that appears in the plugin data dicts, to be used
            for sorting the list. Default: ``plugin_name``

    Returns:
        list of plugin data dicts, sorted by the ``sort_key``, with the keys from the
        input dict (``project_name``) included in the plugin data dicts under the key
        ``plugin_key``. By default, the list is sorted alphabetically by ``plugin_name``.

    """
    plugins_to_sort = []
    for plugin_key, plugin_data in plugins.items():
        plugin_data = plugin_data.copy()
        plugin_data['plugin_key'] = plugin_key
        plugins_to_sort.append(plugin_data)

    return sorted(plugins_to_sort, key=lambda x: x[sort_key])


def normalize_tag(tag: str) -> str:
    """Tag normalization based on the default sphinx-tags behavior.

    Replace whitespace and other non-alphanumeric characters with dashes. See:
    https://github.com/melissawm/sphinx-tags/blob/main/src/sphinx_tags/__init__.py#L293

    Example: 'Tag:with (special   characters) ' -> 'tag-with-special-characters'
    """
    char = "-"
    return re.sub(r"[\s\W]+", char, tag).lower().strip(char)


def plugin_type_display_name(tag: str) -> str:
    """Fetch the display name for ``plugin_type`` keywords."""
    try:
        return PLUGIN_TYPES[tag]
    except KeyError:
        LOGGER.warning(f"plugin_type {tag} does not appear in PLUGIN_TYPES")
        return tag


def format_authors_maintainers(plugin_data: dict) -> str:
    """Format a string representation of authors and/or maintainers.

    If authors are included, they will be listed first (in the order they
    were listed in the ``pyproject.toml``. If the same name appears in both
    authors and maintainers, that name will only be included once.
    """
    authors_maintainers = (
        plugin_data.get('authors', []) +
        plugin_data.get('maintainers', [])
    )

    # Using a list rather than a set to preserve order
    people = []
    for person in authors_maintainers:
        identifier = person.get('name', person.get('email'))
        if identifier and identifier not in people:
            people.append(identifier)

    return ('; ').join(people)


def truncate_text(text: str, length: int = 300, end: str = "...") -> str:
    """Truncate a string to the specified length."""
    if len(text) <= length:
        return text
    truncated = text[: length - len(end)].rsplit(" ", 1)[0]
    return truncated + end


def main():
    all_plugins = load_plugin_json()
    sorted_plugins = sort_plugins(all_plugins)

    env = Environment(
        loader=FileSystemLoader(JINJA_TEMPLATE_DIR),
        autoescape=select_autoescape()
    )

    env.filters['normalize_tag'] = normalize_tag
    env.filters['plugin_type_display_name'] = plugin_type_display_name
    env.filters['format_authors_maintainers'] = format_authors_maintainers
    env.filters['truncate_text'] = truncate_text

    template = env.get_template('plugin_index.html')
    rendered_template = template.render(plugins=sorted_plugins)

    with open(OUTPATH, 'w') as f:
        f.write(rendered_template)


if __name__ == '__main__':
    main()
