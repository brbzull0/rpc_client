from setuptools import find_packages, setup
from distutils.util import convert_path

#main_ns = {}
#ver_path = convert_path('jsonrpc_client/version.py')
# with open(ver_path) as ver_file:
#    exec(ver_file.read(), main_ns)

setup(
    name='jsonrpc',
    # packages=find_packages(include=['jsonrpc_client']),
    version='1'
    description='JSONRPC 2.0 client',
    author='',
    license='APACHE 2.0',
    setup_requires=[],
    #    tests_require=['unittest'],
    #    test_suite='unittest',
    packages=['jsonrpc.*']
)
