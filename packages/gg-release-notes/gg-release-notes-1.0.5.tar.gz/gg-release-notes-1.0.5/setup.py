"""Python setup.py for project_name package"""
import io
import os
from setuptools import find_packages, setup

from release_notes.package_version import __version__ as release_version


def read(*paths, **kwargs):
    """Read the contents of a text file safely."""
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="gg-release-notes",
    version=release_version,
    description="Python Interface for generating release notes for Github Actions",
    url="https://github.com/DataWiz40/gg-release-notes/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="DataWiz40",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("release_notes/requirements.txt"),
    extras_require={"test": read_requirements("release_notes/requirements-test.txt")},
)
