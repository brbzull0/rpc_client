from setuptools import find_packages, setup
from distutils.util import convert_path


setup(
    name='ts_jsonrpc',
    packages=find_packages(include=['ts_jsonrpc.*']),
    version='0.0.1',
    description='JSONRPC 2.0 client',
    author='',
    license='APACHE 2.0',
    install_requires=['colorama', 'argparse', 'pyyaml'],
    setup_requires=[],
    tests_require=['unittest'],
    test_suite='unittest',
    entry_points={
        'console_scripts': [
            'tscli = ts_jsonrpc.cli.cli.main:main'
        ]
    }
)
