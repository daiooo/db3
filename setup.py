# coding=utf-8

import os
from setuptools import setup, find_packages
from ssdb import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='db3',
    version=__version__,
    description='Python 3 client for SSDB',
    long_description=open('README.md').read(),
    url='https://github.com/daiooo/db3',
    author='daiooo',
    author_email='daiooo@dai3.com',
    maintainer='daiooo',
    maintainer_email='daiooo@dai3.com',
    zip_safe=False,
    include_package_data=True,
    keywords=['SSDB'],
    # license='BSD-2',
    install_requires=['pyssdb'],  # 依赖模块
    packages=['ssdb'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ]
)
