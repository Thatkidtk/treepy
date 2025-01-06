# docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'RPTree'
copyright = '2025, Your Name'
author = 'Your Name'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
    'undoc-members': True,
}
