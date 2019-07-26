import os
import re
from setuptools import setup, find_packages


def long_description():
	try:
		return open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
	except IOError:
		return None


def read_version():
	with open(os.path.join(os.path.dirname(__file__), 'layblr', '__init__.py')) as handler:
		return re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", handler.read(), re.M).group(1)


def read_requirements(filename):
	with open(os.path.join(os.path.dirname(__file__), filename), 'r') as handler:
		return [line for line in handler.readlines() if not line.startswith('#') and not line.startswith('-') and not len(line) <= 1]


EXCLUDE_FROM_PACKAGES = [
	'docs*',
	'env*',
	'tests*',
	'src*',
	'e2e*',
	'node_modules*',
]

PKG = 'layblr'
######
setup(
	name=PKG,
	version=read_version(),
	description='Browser based audio feature tagger',
	long_description=long_description(),
	keywords='',
	license='GNU General Public License v3 (GPLv3)',
	packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
	package_data={
		'layblr': [
			'dist/**'
		]
	},
	install_requires=read_requirements('requirements.txt'),
	tests_require=read_requirements('requirements-dev.txt'),
	extras_require={},
	# test_suite='tests',
	include_package_data=True,

	scripts=['layblr/bin/layblr'],
	entry_points={'console_scripts': [
		'layblr = layblr.stamp:execute_from_cli',
	]},

	author='Tom Valk',
	author_email='tomvalk@lt-box.info',

	classifiers=[
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Development Status :: 4 - Beta',

		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3 :: Only',

		'Operating System :: OS Independent',

		'Topic :: Internet',
		'Topic :: Software Development :: Libraries :: Python Modules',

		'Intended Audience :: Developers',

	],
	zip_safe=False,
)
