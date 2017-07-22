.PHONY: docs

init:
	pip install -r requirements.txt

test:
	pyenv local 2.7.12 3.5.3 3.6.1
	tox

test-readme:
	@python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and HISTORY.rst ok") || echo "Invalid markup in README.rst or HISTORY.rst!"

flake8:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 wechatsogou

#publish:
#	pip install 'twine>=1.5.0'
#	python setup.py sdist bdist_wheel
#	twine upload dist/*
#	rm -fr build dist .egg requests.egg-info
