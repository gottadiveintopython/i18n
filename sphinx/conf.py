# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.metadata

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'i18n'
copyright = '2023, Mitō Nattōsai'
author = 'Mitō Nattōsai'
release = importlib.metadata.version('kivy_garden.i18n')
rst_epilog = """
.. |ja| replace:: 🇯🇵
.. _gettext: https://www.gnu.org/software/gettext/
"""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    # 'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    # 'sphinx_tabs.tabs',

]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'en'
add_module_names = False
gettext_auto_build = False
gettext_location = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "alabaster"
html_static_path = ['_static']
html_theme_options = {
    'page_width': '1200px',
    # 'sidebar_width': '400px',
}


# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration
todo_include_todos = True


# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'kivy': ('https://kivy.org/doc/master', None),
}


# -- Options for autodoc extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
autodoc_mock_imports = ['kivy', ]
# autodoc_default_options = {
#    'members': True,
#    'undoc-members': True,
#    'no-show-inheritance': True,
# }
autodoc_class_signature = 'separated'
autodoc_type_aliases = {
    'Msgid': 'Msgid',
    'Msgstr': 'Msgstr',
    'Lang': 'Lang',
    'Translator': 'Translator',
    'TranslatorFactory': 'TranslatorFactory',
    'Font': 'Font',
    'FontPicker': 'FontPicker',
}
