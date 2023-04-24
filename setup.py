from setuptools import find_packages, setup

setup(
    name='comm',
    packages=find_packages(include=['comm']),
    version='0.1.0',
    description='Common code snippets',
    author='marin-jovanovic',
    license='MIT',
    Install_requires=['python-decouple==3.8'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)