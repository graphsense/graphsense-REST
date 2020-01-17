from setuptools import find_packages, setup

name = 'gsrest'
version = '0.4.3.dev'
setup(
    name=name,
    version=version,
    author='GraphSense Team',
    author_email='contact@graphsense.info',
    url='https://github.com/graphsense/graphsense-REST/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-restplus',
        'pyjwt'
    ],
)
