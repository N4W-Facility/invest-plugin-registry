ENV := env
env:
	python3 -m venv $(ENV)
	$(ENV)/bin/python -m pip install -r requirements.txt

all: env
	$(ENV)/bin/python scripts/collect-metadata.py
	$(ENV)/bin/python scripts/convert-metadata-to-rst.py html/metadata.json source/plugins
	make -C source html

