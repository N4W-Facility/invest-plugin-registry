ENV := env
env:
	python3 -m venv $(ENV)
	$(ENV)/bin/python -m pip install -r requirements.txt

all: env
	$(ENV)/bin/python scripts/collect-metadata.py
	$(ENV)/bin/python scripts/convert-metadata-to-rst.py html/metadata.json source/plugins
	$(ENV)/bin/python source/flask/freeze.py
	cp source/flask/build/plugins_index.html source/plugins/
	SPHINXBUILD=$(shell pwd)/$(ENV)/bin/sphinx-build make -C source html
	cp -r source/_build/html/* html

.PHONY: html
html:
	$(ENV)/bin/python scripts/convert-metadata-to-rst.py html/metadata.json source/plugins
	SPHINXBUILD=$(shell pwd)/$(ENV)/bin/sphinx-build make -C source html
	cp -r source/_build/html/* html

.PHONY: freeze
freeze:
	$(ENV)/bin/python source/flask/freeze.py
	cp source/flask/build/plugins_index.html source/plugins/
