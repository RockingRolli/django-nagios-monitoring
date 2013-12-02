import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-nagios-monitoring',
    version='0.1',
    packages=['nagios_monitoring'],
    include_package_data=True,
    license='MIT License', # example license
    description='monitoring for django commands',
    long_description=README,
    url='http://rvo.name/',
    author='Roland von Ohlen',
    author_email='webwork@rvo.name',
    install_requires=['django'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)