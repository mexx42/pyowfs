# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Marcus Priesch, All rights reserved
# In Prandnern 31, A--2122 Riedenthal, Austria. office@priesch.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    setup
#
# Purpose
#    distutils setup
#
# Revision Dates
#    22-Dec-2009 (MPH) Creation
#    18-Mar-2010 (MPH) Version bump to 0.1.1
#    ««revision-date»»···
#--

from distutils.core import setup

setup \
    ( name             = 'pyowfs'
    , version          = '0.1.3'
    , description      = "OWFS' libowcapi wrapper using ctypes"
    , long_description = "This package provides one module with a thin "
      "wrapper around libowcapi and a slightly smarter wrapper around it "
      "for easy access to the 1wire devices. It is inspired by the "
      "OWFS provided python bindings but, however is neither api compatible "
      "nor will it try to be in the future - at least i hope so ;)"
    , author           = 'Marcus Priesch'
    , author_email     = 'marcus@priesch.co.at'
    , url              = 'http://priesch.co.at/pyowfs'
    , packages         = ['pyowfs']
    , requires         = ["ctypes(>1.0.2)"]
    , license          = "LGPL"
    , platforms        = ["POSIX"]
    , classifiers      = \
          [ 'Development Status :: 4 - Beta'
          , 'Environment :: Console'
          , 'Intended Audience :: Developers'
          , 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)'
          , 'Operating System :: Microsoft :: Windows'
          , 'Operating System :: POSIX'
          , 'Programming Language :: Python'
          , 'Topic :: Software Development'
          ]
    )

### __END__ setup


