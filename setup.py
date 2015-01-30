#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install import install

VERSION="0.1"

long_desc = open("README.md").read()

setup(
    name='btponto',
    url='http://code.google.com/p/osantana-code/wiki/BtPonto',
    description='Software to register presence based in Bluetooth device proximity.',
    download_url='http://osantana-code.googlecode.com/files/btponto-%s.tar.gz' % (VERSION,),
    long_description=long_desc,
    author='Osvaldo Santana Neto',
    author_email='btponto@osantana.me',
    version=VERSION,
    scripts=['btponto.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
