#!/usr/bin/env python

import os
from os import path

from setuptools import find_packages, setup

# The directory containing this file
_PATH_ROOT = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(_PATH_ROOT, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="meteron",
    version="0.1.0",
    description='Queuing, storage, metering, rate limiting for AI',
    author='Karolis Rusenas',
    author_email='karolis@rusenas.dev',
    url='https://meteron.com',
    download_url="https://github.com/meteron-ai/meteron-python",
    license='Apache License 2.0',
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    keywords=["deep learning", "ML", "AI"],
    python_requires=">=3.8",
    setup_requires=["wheel"],
    install_requires=["requests>=2.28.2"],
)