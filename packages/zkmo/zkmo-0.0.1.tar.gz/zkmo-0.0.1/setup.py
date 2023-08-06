#!/usr/bin/env python3
import os
import re
import sys
from io import open

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

# Check Python Version.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of Bossjob Comm requires Python {}.{}, but you're trying
to install it on Python {}.{}.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)


def read(f):
    return open(f, "r", encoding="utf-8").read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version("zkmo")

setup(
    name="zkmo",
    version=version,
    url="https://www.bossjob.ph/",
    description="zkmo",
    long_description=read("README.md"),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "requests"
    ],
    python_requires=">=3.7",
    zip_safe=False,
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    project_urls={
        "Source": "https://github.com/zekeeol/zkmo",
    },
)
