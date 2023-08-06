from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.0'

setup(
    name='sihodictapi',  # package name
    version=VERSION,  # package version
    description='一些在线词典/翻译API',  # package description
    packages=find_packages(),
    zip_safe=False,
)
