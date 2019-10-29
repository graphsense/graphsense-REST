from setuptools import find_packages, setup

setup(
    name='gsrest',
    version='0.4.2-dev',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-restplus',
        'pyjwt'
    ],
)
