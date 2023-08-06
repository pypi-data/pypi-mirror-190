"""Describe our module distribution to Distutils."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from setuptools import find_packages
from setuptools import setup

setup(
    name="arthub_login_widgets",
    version="0.2.3",
    author="Joey Ding",
    author_email="Hallong@tencent.com",
    url="https://git.woa.com/lightbox/internal/arthub_login_widgets",
    package_dir={"": "."},
    packages=find_packages("."),
    description="A Qt Widget for login ArtHub.",
    entry_points={},
    package_data={"": ["*.png", "*.qss"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["arthub_api", "platformdirs==2.0.2"]
)
