"""Sphinx docs config."""

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
from __future__ import annotations

import pre_commit_hooks as py_pkg

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "5.0.0"

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    # External
    "sphinx_copybutton",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10", None),
}

autodoc_default_options = {
    "member-order": "bysource",
    "members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "undoc-members": True,
}
autodoc_inherit_docstrings = False

# nitpick_ignore = []

# Add any paths that contain templates here, relative to this directory.
# templates_path = []

# The suffix of source filenames.
source_suffix = ".rst"

# General information about the project.
project = py_pkg.__name__
copyright = ", "

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = py_pkg.__version__
# The full version, including alpha/beta/rc tags.
release = py_pkg.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
today = "1"
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "furo"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the documentation.
# https://pradyunsg.me/furo/customisation/
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = []

# html_style = ""

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"


# -- Options for Napoleon  -----------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False  # Explicitly prefer Google style docstring
napoleon_use_param = True  # for type hint support
napoleon_use_rtype = False  # False so the return type is inline with the description.
