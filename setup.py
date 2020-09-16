from setuptools import find_packages, setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('ts_jsonrpc/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='ts_jsonrpc',
    packages=find_packages(include=['ts_jsonrpc.*']),
    version=main_ns['__version__'],
    description='JSONRPC 2.0 client',
    author='',
    license='APACHE 2.0',
    install_requires=['colorama', 'argparse'],
    setup_requires=[],
    tests_require=['unittest'],
    test_suite='unittest',
    entry_points={
        'console_scripts': [
            'tscli = ts_jsonrpc.cli.cli.main:main'
        ]
    }
)
