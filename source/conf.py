# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'InVEST Plugins Registry'
copyright = '2026, The Natural Capital Alliance'
author = 'The Natural Capital Alliance'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_design",
    "sphinx_tags",
    "sphinx_copybutton",
    "myst_parser",
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'jinja']


# -- Sphinx Tags Config ------------------------------------------------------
tags_create_tags = True
tags_create_badges = True
tags_intro_text = ''
tags_overview_title = "All Plugin Registry Keywords"
tags_page_header = 'With this keyword'
tags_page_title = 'Keyword'
tags_badge_colors = {
    "Preprocessing": "primary",
    "Postprocessing": "primary",
    "Workflow": "primary",
    "InVEST Model Variant": "primary",
    "New Model": "primary",
    "Other": "primary",
    "*": "info"
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'  # pip install furo
html_favicon = "_static/favicon.png"
html_title = "InVEST Plugin Registry"
html_static_path = ['_static']
html_theme_options = {
    'light_logo': 'alliance-logo-full-color.png',
    'dark_logo': 'alliance-logo-full-white.png',
    'light_css_variables': {
        'color-brand-primary': '#175e54',
        'color-brand-content': '#2e2d29',
        'color-link': '#009ab4',
        'color-announcement-background': '#007c92',
        'sd-color-card-border-hover': '#007c92',
        'sd-color-secondary': '#2D716F',
        'sd-color-secondary-highlight': '#014240',
    },
    'dark_css_variables': {
        'color-brand-primary': '#B6B1A9',
        'color-brand-content': '#F4F4F4',
        'color-link': '#009ab4',
        'color-announcement-background': '#620059',
        'sd-color-card-border-hover': '#620059',
        'sd-color-secondary': '#734675',
        'sd-color-secondary-highlight': '#620059',
    },
    'sidebar_hide_name': True,  # don't show name in sidebar, only logo
    'announcement': '',
}
html_css_files = [
    'css/custom.css'
]
