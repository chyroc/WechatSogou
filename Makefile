.PHONY: docs

init:
	pip install -r requirements.txt

flake8:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 wechatsogou

tox:
	pyenv local 2.7.12 3.5.3 3.6.1
	tox
