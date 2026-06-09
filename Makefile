ENV := env
env:
	python3 -m venv $(ENV)
	$(ENV)/bin/python -m pip install -r requirements.txt

all: env
	$(ENV)/bin/python scripts/collect-metadata.py
	$(ENV)/bin/python scripts/convert-metadata-to-rst.py html/metadata.json source/plugins
	$(ENV)/bin/python scripts/build-plugin-index.py
	SPHINXBUILD=$(shell pwd)/$(ENV)/bin/sphinx-build make -C source html
	cp -r source/_build/html/* html
	$(ENV)/bin/python scripts/render-pyodide.py scripts/lint-metadata.py html/_static/pyodide-linting.js

.PHONY: html
html:
	$(ENV)/bin/python scripts/convert-metadata-to-rst.py html/metadata.json source/plugins
	$(ENV)/bin/python scripts/build-plugin-index.py
	SPHINXBUILD=$(shell pwd)/$(ENV)/bin/sphinx-build make -C source html
	cp -r source/_build/html/* html
