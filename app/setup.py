#!/usr/bin/env python

from setuptools import setup
import os

setup(
    name='EnvironmentMonitor',
    version='0.1',
    description='A residential environment monitoring system that records temperature, humidity and moisture around the house.',
    author='DeckerEgo',
    author_email='deckerego@gmail.com',
    url='https://github.com/deckerego/EnvironmentMonitor',
    packages=[''],
    long_description=open('../README.md').read(),
    data_files=[
        ('views',    [os.path.join('views', 'index.tpl')]),
        ('views/css',[os.path.join('views/css', 'styles.css')])
    ],
    classifiers=[
    	"License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    	"Programming Language :: Python",
    	"Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
    	"Topic :: Home Automation"
    ],
    keywords='motion security surveillance garage remote raspberrypi',
    requires=[
        'bottle (==0.10.11)',
        'sleekxmpp (>=1.0)'
    ],
	)
