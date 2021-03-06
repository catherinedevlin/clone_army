#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests>=2.10',
    'Click>=6.0',
]

test_requirements = [
]

setup(
    name='clone_army',
    version='0.2.0',
    description="Locally clone or synch all a GitHub account's repos",
    long_description=readme + '\n\n' + history,
    author="18F",
    author_email='catherine.devlin@gsa.gov',
    url='https://github.com/18F/clone_army',
    packages=[
        'clone_army',
    ],
    package_dir={'clone_army':
                 'clone_army'},
    entry_points={
        'console_scripts': [
            'clone-army=clone_army.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="CC0 license",
    zip_safe=False,
    keywords=['git', 'repository', 'clone'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
