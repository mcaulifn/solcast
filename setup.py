#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import setuptools_scm

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = ['pytest>=3', ]


def local_scheme(version):
    print(version)
    if version.branch == 'master' and not version.dirty:
        return ''
    return setuptools_scm.version.get_local_node_and_date(version)


setup(
    author="Nathaniel McAuliffe",
    author_email='nathanielmcauliffe@hotmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Solcast API",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='solcast',
    name='pysolcast',
    packages=find_packages(include=['pysolcast', 'pysolcast.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mcaulifn/solcast',
    use_scm_version={
        'local_scheme': local_scheme,
        'write_to': '',
        'write_to_template': '__version__ = "{version}"\n',
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$'
    },
    version='1.0.0',
    zip_safe=False,
)
