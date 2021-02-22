#!/usr/bin/env python3

# Monkey-patches setuptools to generate faster entry-point script.
import fastentrypoints

from os.path import join, dirname
from setuptools import setup, find_packages

with open(join(dirname(__file__), 'requirements.txt')) as r:
    requirements = [l.strip() for l in r]

setup(
    name='k8s-image-updater',
    packages=find_packages(),
    # Create executable named k8s-image-updater
    entry_points={
        'console_scripts': [
            'k8s-image-updater = updater.main:main',
        ],
    },
    # Include requirements.txt
    install_requires=requirements,
    # Non-Python files
    include_package_data=True,
)
