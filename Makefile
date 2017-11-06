.PHONY: doc dry_publish

docdir = docs
doc:
	if [ -a $(docdir)/README.rst ]; then rm $(docdir)/README.rst; fi;
	pandoc --from=markdown --to=rst --output=$(docdir)/README.rst README.md
	if [ -a $(docdir)/HISTORY.rst ]; then rm $(docdir)/HISTORY.rst; fi;
	pandoc --from=markdown --to=rst --output=$(docdir)/HISTORY.rst CHANGELOG.md
	python setup.py check --restructuredtext

dry_publish:
	rm -rf dist/ build/
	python setup.py sdist bdist_wheel

publish: dry_publish
	twine upload -s dist/*

flake8:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 wechatsogou

tox:
	pyenv local 2.7.12 3.5.3 3.6.1
	tox

clean:
	@rm -rf build/ wechatsogou.egg-info/ dist/