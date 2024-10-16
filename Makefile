.PHONY: clean help \
	requirements selfcheck upgrade docs serve_docs

.DEFAULT_GOAL := help

# For opening files in a browser. Use like: $(BROWSER)relative/path/to/file.html
BROWSER := python -m webbrowser file://$(CURDIR)/

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

# Define PIP_COMPILE_OPTS=-v to get more information during make upgrade.
PIP_COMPILE = pip-compile --upgrade $(PIP_COMPILE_OPTS)

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -r requirements/pip-tools.txt
	# Make sure to compile files after any other files they include!
	$(PIP_COMPILE) -o requirements/pip-tools.txt requirements/pip-tools.in
	$(PIP_COMPILE) -o requirements/doc.txt requirements/doc.in

requirements: ## install development environment requirements
	pip install -r requirements/pip-tools.txt -r requirements/doc.txt

docs: ## build the documentation
	cd docs && $(MAKE) html

serve_docs: ## serve the built docs locally to preview the site in the browser
	cd docs && $(MAKE) serve_docs

selfcheck: ## check that the Makefile is well-formed
	@echo "The Makefile is well-formed."
