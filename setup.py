# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "24.04.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.6.0",
    "swagger-ui-bundle>=0.0.6",
    "aiohttp_jinja2>=1.2.0",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="GraphSense API",
    author_email="contact@ikna.io",
    keywords=["OpenAPI", "GraphSense API"],
    python_requires='>=3.8',
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/graphsense/graphsense-REST/',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

