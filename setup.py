#!/usr/bin/env python
# -----------------------------------------------------------------------------
#    Kakuch - Traffic wrapper application
#    Copyright (C) 2013 Sameer Rahmani <lxsameer@gnu.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from distutils.core import setup

setup(name='Kakuch',
      version='0.1.0',
      description='Traffic wrapper application',
      author='Sameer Rahmani',
      author_email='lxsameer@gnu.org',
      url='http://kakuch.karajlug.org/',
      download_url="http://kakuch.karajlug.org/downloads/",
      keywords=('wrapper', 'traffic', 'transport'),
      license='GPL v2',
      scripts=["kakuchd"],
      packages=['kakuch', ],
      install_requires=['twisted', 'pyopenssl', 'pycrypto'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
          ]
)
