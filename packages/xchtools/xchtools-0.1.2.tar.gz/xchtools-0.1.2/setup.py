from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.2'

setup(
    name='xchtools',  # package name
    version=VERSION,  # package version
    description="xch's tools",  # package description
    author='xch',
    packages=find_packages(),
    zip_safe=False,
)