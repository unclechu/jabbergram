#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.1.6'

setup(name='jabbergram',
      version=VERSION,
      description='XMPP/Jabber - Telegram Gateway.',
      long_description=open('README.rst', encoding='utf-8').read(),
      author='drymer',
      author_email='drymer@autistici.org',
      url='http://daemons.cf/cgit/jabbergram/about/',
      download_url='http://daemons.cf/cgit/jabbergram/snapshot/jabbergram-' + VERSION + '.tar.gz',
      scripts=['jabbergram.py'],
      license="GPLv3",
      install_requires=[
          "sleekxmpp>=1.3.1",
          "python-telegram-bot>=4.0.3",
          "requests>=2.11.1",
          ],
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Operating System :: OS Independent",
                   "Operating System :: POSIX",
                   "Intended Audience :: End Users/Desktop"]
      )
