import sys

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tcurtis.pysandbox",
    version="1.0.001",
    author_email="tjcurt@gmail.com",
    license="MIT",
    description="Tyler's collection of python scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["*.tests"]),
    package_data={ "": ["*.txt"], },
    install_requires=["tox"],
    classifiers=["Programming Language :: Python :: 3.9+", "Operating System :: OS Independent"],
    entry_points={
        "console_scripts": [
            "spelling-bee = pysandbox.spelling_bee:main",
        ]
    },
)
