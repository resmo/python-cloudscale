from __future__ import unicode_literals

from codecs import open
from setuptools import find_packages, setup
from cloudscale import __version__

install_requires = ['requests', 'click', 'tabulate']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cloudscale-cli",
    version=__version__,
    author="Rene Moser",
    author_email="mail@renemoser.net",
    description="A command line interface for cloudscale.ch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/resmo/cloudscale-cli",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'cloudscale-cli = cloudscale.cli:cli',
        ],
    },
)
