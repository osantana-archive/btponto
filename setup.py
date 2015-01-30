#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install import install

VERSION="0.1"

setup(
    name='btponto',
    url='http://code.google.com/p/osantana-code/wiki/BtPonto',
    description='Software to register presence based in Bluetooth device proximity.',
    download_url='http://osantana-code.googlecode.com/files/btponto-%s.tar.gz' % (VERSION,),
    long_description="""btponto
=======

This software register your presence based on a discoverable Bluetooth device
that you normaly brings together with you: your cell phone.

To install this software follow the steps below:

1. Install Python 2.5::

   $ sudo apt-get install python2.5 # in Ubuntu Linux

2. Install the Python Bluez::

   $ sudo apt-get install python-bluez

3. Run the install script::

   $ sudo python2.5 setup.py install

4. Add the ``btponto.crontab`` example in your crontab.

Changelog
---------

- **2007-06-01** - 0.1 - First release.

To-Do List
----------

- Check the state sanity
- Discard invalid registers in log file

Please, send your bug reports, informations, doubts and other feedbacks to::

    osantana
    <at>
    gmail com
    """,
    author='Osvaldo Santana Neto',
    author_email='osantana@gmail.com',
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
