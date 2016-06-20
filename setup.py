#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup

setup(name='rheem_controller',
	version='1.0',
	description='',
	author='Steven Presser',
	author_email='rheem_controller@pressers.name',
	url='https://github.com/spresse1/rheem_controller',
	packages=['rheem_controller'],
	requires=[
	],
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Environment :: No Input/Output (Daemon)",
		"Environment :: Web Environment",
		"Framework :: Paste",
		"Intended Audience :: Developers",
		"Intended Audience :: System Administrators",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python :: 2.7",
		"Topic :: Internet :: Proxy Servers",
		"Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
		"Topic :: Software Development :: Libraries",
	],
	setup_requires=['pytest-runner', ],
	tests_require=[
		'pytest',
		"coverage",
		"mock",
		"tox",
	],
)
