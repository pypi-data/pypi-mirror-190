import setuptools
from setuptools import setup

setup(
    name = 'mylibtest',
    version = '0.1',
    author = 'BYManbu',
    url = 'https://pypi.org/help/',
    packages = setuptools.find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"],include=["sub_package"]) #setuptools.find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
)