from setuptools import setup

setup(
    # Application name:
    name="Fibonacci Micro-service",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="John Gomez",
    author_email="johncar@gmail.com",

    # Packages
    packages=["fibonacci"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/FibonacciMicroservice_v010/",

    #
    license="MIT",
    description="A sample of microservice in python",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "Flask>=0.2",
        "Celery>=3.1"
    ],

    # List additional groups of dependencies  (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'fibonacci=fibonacci:main',
        ],
    },
)