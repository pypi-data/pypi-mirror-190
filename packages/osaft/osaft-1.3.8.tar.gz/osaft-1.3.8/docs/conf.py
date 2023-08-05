# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
from __future__ import annotations
from sphinx.ext.autodoc import ClassDocumenter, bool_option
from sphinx_gallery.sorting import ExplicitOrder, FileNameSortKey
from autoclasstoc.sections import PublicMethods
from docutils.statemachine import StringList
from typing import Any
from enum import IntEnum
import sys
import os
import re
import time
import codecs
import os.path

sys.path.insert(0, os.path.abspath(".."))


def reset_plotting(gallery_conf, fname):
    """Resetting line style after each example"""
    from matplotlib import pyplot as plt

    plt.style.use("seaborn-muted")
    plt.rcParams.update({"font.size": 12})
    from osaft.plotting.datacontainers.arf_datacontainer import ARFData

    ARFData._instances = 0


class PublicMethodsExclusive(PublicMethods):
    """
    Include a "Public Methods" section in the class TOC.
    """

    key = "public-methods-exclusive"
    title = "Public Methods:"

    def predicate(self, name, attr, meta):
        out = PublicMethods.predicate(self, name, attr, meta)
        out = out and name[0] != "_"
        return out


class IntEnumDocumenter(ClassDocumenter):
    objtype = "intenum"
    directivetype = ClassDocumenter.objtype
    priority = 10 + ClassDocumenter.priority
    option_spec = dict(ClassDocumenter.option_spec)
    option_spec["hex"] = bool_option

    @classmethod
    def can_document_member(
        cls,
        member: Any,
        membername: str,
        isattr: bool,
        parent: Any,
    ) -> bool:
        try:
            return issubclass(member, IntEnum)
        except TypeError:
            return False

    def add_directive_header(self, sig: str) -> None:
        super().add_directive_header(sig)
        self.add_line("   :final:", self.get_sourcename())

    def add_content(
        self,
        more_content: None | StringList,
    ) -> None:

        super().add_content(more_content)

        source_name = self.get_sourcename()
        enum_object: IntEnum = self.object
        use_hex = self.options.hex
        self.add_line("", source_name)

        for the_member_name, enum_member in enum_object.__members__.items():
            the_member_value = enum_member.value
            the_member_doc = enum_member.__doc__
            if use_hex:
                the_member_value = hex(the_member_value)

            self.add_line(
                f"**{the_member_name}**: {the_member_doc}",
                source_name,
            )
            self.add_line("", source_name)


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        match = re.search(r"## (\d{1,2}\.\d{1,2}\.\d{1,2})", line)
        if match is not None:
            match = match.group(1)
            return str(match)
    else:
        raise RuntimeError("Unable to find version string.")


# -- Project information -----------------------------------------------------


project = "osaft"
copyright = f'{time.strftime("%Y")}, Fankhauser&Goering'
author = "Jonas Fankhauser & Christoph Goering "

# The full version, including alpha/beta/rc tags
release = get_version("../CHANGELOG.md")


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "autoclasstoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
    "sphinx_autodoc_defaultargs",
    "sphinx_copybutton",
    "sphinx_gallery.gen_gallery",
]

autosummary_generate = True

autodoc_default_optiony = {
    "members": True,
    "special-members": False,
    "private-members": False,
    "inherited-members": True,
    "undoc-members": False,
    "exclude-members": ["__weakref__", "__init__", "__repr__", "__str__"],
}
autoclasstoc_sections = [
    "public-attrs",
    "public-methods-exclusive",
]

# change this to True to update the allowed failures
missing_references_write_json = False
missing_references_warn_unused_ignores = False

intersphinx_mapping = {
    "matplotlib": ("https://matplotlib.org/stable", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}


# sphinx_gallery
sphinx_gallery_conf = {
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "examples",  # path to where to save gallery generated
    "filename_pattern": "/example",
    "line_numbers": True,
    "show_memory": True,
    "matplotlib_animations": True,
    "reset_modules": ("matplotlib", reset_plotting),
    # directory where function/class granular galleries are stored
    "backreferences_dir": "backreferences",
    # Modules for which function/class level galleries are created.
    "doc_module": ("osaft"),
    "reference_url": {
        "osaft": None,
    },
    "prefer_full_module": [r"osaft.solutions.\w+\d{4}\w*"],
    "subsection_order": ExplicitOrder(
        [
            "../examples/publication/",
            "../examples/validation/",
            "../examples/tutorial/",
        ],
    ),
    "within_subsection_order": FileNameSortKey,
}

# shpinx_copybutton configuration
copybutton_prompt_text = r">>> |\.\.\. ?|\s*\d{1,3} ?|"
copybutton_prompt_is_regexp = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**tests**", "_build", "Thumbs.db", ".DS_Store"]


# Ensure that the __init__ method gets documented.
#  def skip(app, what, name, obj, skip, options):
#      if name == "__repr__" or name == "__str__":
#          return False
#      return skip


def setup(app):
    #  app.connect("autodoc-skip-member", skip)
    app.add_css_file("_static/custom.css")
    app.setup_extension("sphinx.ext.autodoc")  # Require autodoc extension
    app.add_autodocumenter(IntEnumDocumenter)


#  always_document_param_types (default: False): If False, do not add type info
#  for undocumented parameters. If True, add stub docu for undocumented
#  parameters to be able to add type info.
always_document_param_types = True

# add padding around inheritance diagrams
inheritance_graph_attrs = dict(pad=0.4, rankdir="TB", size='""')

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_js_files = ["custom.js"]
#
html_theme = "furo"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_theme_options = {
    "navigation_with_keys": True,
    "light_css_variables": {
        "color-brand-primary": "#ee7029",
        "color-brand-content": "green",
        "color-admonition-background": "white",
        "color-api-pre-name": "#ee7029",
    },
    "footer_icons": [
        {
            "name": "GitLab",
            "url": "https://gitlab.com/acoustofluidics/osaft",
            "html": "",
            "class": "fa-brands fa-gitlab fa-2x",
        },
    ],
}
html_favicon = "_static/osaft.ico"

# font-awesome logos
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",  # noqa: E501
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",  # noqa: E501
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",  # noqa: E501
    "custom.css",
]

# Sort members by type
autodoc_member_order = "groupwise"
#  autodoc_member_order = 'bysource'

# Formatting for sphinx_autodoc_defaultargs
rst_prolog = (
    """
.. |default| raw:: html

    <div class="default-value-section">"""
    + '<span class="default-value-label"'
    + 'style="color: rgb(179, 0, 0);">Default: </span>'
)
