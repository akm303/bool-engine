from setuptools import find_packages, setup

setup(
    name='bool-engine',
    packages=find_packages(include=['bool-engine']),
    version='1.1',
    description='Custom Python Library For Boolean Logic Solvers and Truth Table Operations',
    author='Ari Majumdar',
    url='https://github.com/akm303/bool-engine',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)