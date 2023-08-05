# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -j auto
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile


# detect what shell is used
ifeq ($(findstring cmd.exe,$(SHELL)),cmd.exe)
$(info "shell Windows cmd.exe")
DEVNUL := NUL
WHICH := where
else
$(info "shell Bash")
DEVNUL := /dev/null
WHICH := which
endif

# detect platform independently if gcc is installed
ifeq ($(shell ${WHICH} dot 2>${DEVNUL}),)
$(error "dot is not in your system PATH. Please install it and put it into your PATH")
$(error "http://graphviz.org")
else
$(info "dot (graphviz) found")
endif

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf examples/
	rm -rf **/generated/
	rm -rf generated/
	rm -rf backreferences/

show:
	@python3 -c "import webbrowser; webbrowser.open_new_tab('file://$(shell pwd)/_build/html/index.html')"
