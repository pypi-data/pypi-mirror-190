from setuptools import find_packages, setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='codified_json',
    packages=find_packages(include=['codified_json']),
    description='Codified-JSON - represent the same JSON data with less characters',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tim Huang',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner==6.0.0', 'setuptools_scm'],
    use_scm_version=True,
    tests_require=['pytest==7.2.0'],
    test_suite='tests'
)