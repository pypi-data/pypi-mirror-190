#!/usr/bin/env python
import os, sys
import shutil
import datetime

from setuptools import setup, find_packages
from setuptools.command.install import install

readme = open('README.md').read()

VERSION = '0.0.1'

# import subprocess
# commit_hash = subprocess.check_output("git rev-parse HEAD", shell=True).decode('UTF-8').rstrip()
# VERSION += "_" + str(int(commit_hash, 16))[:8]
VERSION += "_" + datetime.datetime.now().strftime('%Y%m%d%H%M')[2:]
# print(VERSION) 

setup(
    # Metadata
    name='pktype',
    version=VERSION,
    author='roa0831',
    author_email='',
    url='https://twitter.com/qr1x_while :',
    description='A library for checking Pokemon type compatibility',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',

    # Package info
    packages=find_packages(exclude=('*test*',)), 

    #
    zip_safe=True,
    #nstall_requires=requirements,

    # Classifiers
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
)