#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-newsletter-subscription',
    version=__import__('newsletter_subscription').__version__,
    description='Another newsletter subscription app.',
    long_description=read('README.rst'),
    author='Matthias Kestenholz',
    author_email='mk@406.ch',
    url='http://github.com/matthiask/django-newsletter-subscription/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(),
    package_data={
        '': ['*.html', '*.txt'],
        'newsletter_subscription': [
            'locale/*/*/*.*',
            # 'static/newsletter_subscription/*.*',
            # 'static/newsletter_subscription/*/*.*',
            'templates/*.*',
            'templates/*/*.*',
            'templates/*/*/*.*',
            'templates/*/*/*/*.*',
        ],
    },
    install_requires=[
        'Django>=1.8',
        # Yes, newsletter_subscription can be used without towel. towel is
        # only a requirement if you want to use the bundled templates.
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    zip_safe=False,
)
