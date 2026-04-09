ENV := env
env:
	python3 -m venv $(ENV)
	$(ENV)/bin/python -m pip install -r requirements.txt
