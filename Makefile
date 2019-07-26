
build:
	@ python setup.py sdist
#	@ python setup.py bdist_wheel --python-tag py3

publish:
	@ python setup.py sdist
#	@ python setup.py bdist_wheel --python-tag py3
	@ twine upload dist/layblr-*

run-tox:
	@ tox

tests: run-tox clean

clean:
	@ find . -name '*.py[co]' -delete
	@ find . -name '__pycache__' -delete
	@ rm -rf *.egg-info dist/layblr-* build
