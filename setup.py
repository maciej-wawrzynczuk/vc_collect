#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name="vc_collect",
    version="0.1",
    packages=find_packages(),
    scripts=["vc_collect"],
    install_requires=["pyvmomi"]
)
