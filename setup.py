# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Marcus Priesch, All rights reserved
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
#    22-Dec-2009 (MP) Creation
#    ««revision-date»»···
#--

from distutils.core import setup

setup \
    ( name         = 'pyowfs'
    , version      = '0.1'
    , description  = "OWFS' libowcapi wrapper"
    , author       = 'Marcus Priesch'
    , author_email = 'marcus@priesch.co.at'
    , url          = 'http://www.priesch.co.at/pyowfs'
    , packages     = ['owfs']
    , requires     = ["ctypes(>1.0.2)"]
    )

### __END__ setup


