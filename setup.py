#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-protocolify',
    version='0.1.0',
    description='Template tag to change the protocol of URLs in links.',
    author='Bradley Ayers',
    author_email='bradley.ayers@gmail.com',
    url='https://github.com/bradleyayers/django-protocolify/',

    packages=find_packages(),
    include_package_data=True,  # declarations in MANIFEST.in

    install_requires=['Django >=1.2'],
    tests_require=['Django >=1.2', 'django-attest'],

    test_loader='attest:FancyReporter.test_loader',
    test_suite='tests.everything',

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
