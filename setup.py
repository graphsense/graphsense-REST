import re
from setuptools import find_packages, setup

VERSIONFILE = "gsrest/_version.py"
verfilestr = open(VERSIONFILE, "rt").read()
match = re.search(r"^__version__ = '(\d\.\d.\d+(\.\d+)?)'",
                  verfilestr,
                  re.MULTILINE)
if match:
    version = match.group(1)
else:
    raise RuntimeError(
        "Unable to find version string in {}.".format(VERSIONFILE))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gsrest',
    version=version,
    packages=find_packages(),
    author='GraphSense core team',
    author_email='contact@graphsense.info',
    description='GraphSense REST interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/graphsense/graphsense-REST/',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'flask>=1.1.2',
        'flask-restplus>=0.13.0',
        'pyjwt>=1.7.1',
        'cassandra-driver>=3.23.0',
        'Werkzeug>=0.16.0',
        'pyjwt>=1.7.1'
    ],
    test_suite="tests"
)
