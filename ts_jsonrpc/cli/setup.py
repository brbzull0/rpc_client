from setuptools import find_packages, setup
from distutils.util import convert_path

setup(
    name='tscli',
    version='1'
    description='JSONRPC 2.0 client',
    author='',
    license='APACHE 2.0',
    install_requires=['colorama', 'argparse'],
    setup_requires=[],
    tests_require=['unittest'],
    test_suite='unittest',
    packages=['cli.*']
)
