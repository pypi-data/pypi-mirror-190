"""Python setup.py for tripsim package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("tripsim", "VERSION")
    '0.1.4'
    >>> read("README.md")
    ...
    """

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
    name="tripsim",
    version=read("tripsim", "VERSION"),
    description="Simple driving trip simulator for OpenStreetMap graphs",
    url="https://github.com/nSurely/tripsim/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Inaza",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["tripsim = tripsim.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
    python_requires=">=3.7"
)
