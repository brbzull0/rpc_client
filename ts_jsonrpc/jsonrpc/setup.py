from setuptools import find_packages, setup
from distutils.util import convert_path

setup(
    name='ts_jsonrpc',
    version='1'
    description='JSONRPC 2.0 client',
    author='',
    license='APACHE 2.0',
    setup_requires=[],
    packages=['jsonrpc.*']
)
