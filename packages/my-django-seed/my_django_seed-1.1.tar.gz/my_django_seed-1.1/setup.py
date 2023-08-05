import codecs
import os
import re
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


# Read the version number from a source file.
# Why read it, and not import?
# https://packaging.python.org/en/latest/single_source_version.html
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')


setup(
    name='my_django_seed',
    version=find_version('my_django_seed', '__init__.py'),
    author='Moti shakuri',
    author_email='motishaku@gmail.com',
    packages=['my_django_seed', 'my_django_seed.management', 'my_django_seed.management.commands'],
    include_package_data=True,
    license='MIT',
    description='Seed your Django project with fake data, this is a fork of the original django_seed to support 2.7 with small changes.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords='faker fixtures data test django seed',
    long_description=open('README.rst', 'r').read(),
    install_requires=['django>=1.8', 'Faker>=0.7.7'],
    tests_require=['django>=1.8', 'fake-factory>=0.5.0', 'coverage', 'django-nose'],
    test_suite="runtests.runtests",
    zip_safe=False,
)
