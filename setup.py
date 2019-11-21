#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from codecs import open
from setuptools import find_packages, setup
from cloudscale import __version__

install_requires = []
with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = list(i.rstrip() for i in f.readlines())

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cloudscale",
    version=__version__,
    author="René Moser",
    author_email="mail@renemoser.net",
    license="MIT",
    description="A library and command line interface for cloudscale.ch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/resmo/python-cloudscale",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cloudscale-cli = cloudscale.cli:cli',
        ],
    },
)
