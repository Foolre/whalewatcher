# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='whalewatcher',
    version='0.1.0',
    description='bitcoin exchange watcher with Sample package from Python-Guide.org',
    long_description=readme,
    author='Foolre',
    url='https://github.com/Foolre/whalewatcher',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

