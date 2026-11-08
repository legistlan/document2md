# Configuration file for the Sphinx documentation builder.
#
# For a full list of options see:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup ---------------------------------------------------------
#
# document2md is installed editable (--no-deps) by the workflows that build
# these docs (website.yml, test.yml) rather than reached via sys.path
# manipulation here, so conf.py only needs to import the already-installed
# package to read its __version__.

import document2md

# -- Project information -------------------------------------------------

project = "document2md"
copyright = "2026, legistlan"
author = "legistlan"

# The repository is the package, so there is a single version here — kept as
# the same |document2md_version| substitution the page used while this was
# one page of the LegalIA monorepo's site.
rst_epilog = f"""
.. |document2md_version| replace:: {document2md.__version__}
"""

# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.graphviz",
    "sphinx.ext.doctest",
]

# Render the conversion-pipeline diagram (index.rst) as inline SVG rather than
# a linked PNG, so it stays crisp at any zoom and matches the page background.
graphviz_output_format = "svg"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}
# dofjson and nota2md were split off when document2md was extracted from the
# LegalIA monorepo (issue #233): dofjson now lives at
# https://github.com/legistlan/dofjson, nota2md still in the LegalIA
# repository. They are what feeds document2md a PDF and what calls it at all,
# and they are written as plain external links rather than cross-resolved
# through intersphinx, because neither publishes an objects.inv (an entry for
# either would only warn on every build while resolving nothing). Once one
# does, adding it to the mapping above, plus :py:func:/:py:mod: roles on its
# names, is all it takes.

source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = []

pygments_style = "sphinx"
highlight_language = "python"
autodoc_member_order = "bysource"
autodoc_class_signature = "separated"
add_function_parentheses = False
add_module_names = False

# document2md never imports mineru itself in-process — it only shells out to the
# mineru-api CLI as a subprocess (see document2md/mineru_server.py) — and
# document2md/pymupdf_backend.py imports pymupdf/pymupdf4llm lazily, inside
# functions rather than at module level, so autodoc needs no mock for either;
# document2md is installed with --no-deps in website.yml and test.yml precisely
# so neither the heavy mineru[pipeline] install (and its libgl1/opencv system
# dependency, see .github/workflows/test.yml) nor pymupdf4llm ever has to
# happen for a docs build.

# -- Options for HTML output ----------------------------------------------

html_theme = "furo"
html_title = "document2md"
htmlhelp_basename = "document2mddoc"

# -- Options for LaTeX/manual/texinfo output -------------------------------

latex_documents = [
    (master_doc, "document2md.tex", "document2md Documentation", author, "manual"),
]
man_pages = [(master_doc, "document2md", "document2md Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        "document2md",
        "document2md Documentation",
        author,
        "document2md",
        "Convert a PDF or a set of scanned page images to Markdown via OCR.",
        "Miscellaneous",
    ),
]
