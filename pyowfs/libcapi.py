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
#    libcapi
#
# Purpose
#    Wrapper for OWFS' libcapi
#
# Revision Dates
#    22-Dec-2009 (MPH) Creation
#    18-Mar-2010 (MPH) Changed to use ctypes.cdll.LoadLibrary instead of
#                      ctypes.CDLL to honor LD_LIBRARY_PATH
#    ««revision-date»»···
#--
import ctypes
import sys

class AlreadyInitialisedError (StandardError) :
    pass
# end class AlreadyInitialisedError

class CAPI (object) :
    def __init__ (self) :
        if sys.platform == "linux2" :
            self.libcapi = ctypes.cdll.LoadLibrary ("libowcapi.so")
            self.libc    = ctypes.CDLL ("libc.so.6")
        else :
            raise NotImplementedError ("No support for %r" % sys.platform)

        self.ow = None
    # end def __init__

    def init (self, params) :
        self.init_params = params
        if self.ow is not None :
            raise AlreadyInitialisedError

        self.ow = self.libcapi.OW_init (params)
    # end def init

    def finish (self) :
        self.libcapi.OW_finish ()
        self.ow = None
    # end def finish

    def reinit (self) :
        if self.ow :
            self.finish ()
        self.init (self.init_params)
    # end def reinit

    def get (self, path) :
        buf_p   = ctypes.POINTER (ctypes.c_char) ()
        buf_len = ctypes.c_long ()
        res = self.libcapi.OW_get \
            (path, ctypes.byref (buf_p), ctypes.byref (buf_len))
        if res >= 0 :
            res = "".join ([i for i in buf_p [:buf_len.value]])
            self.libc.free (buf_p)
        else :
            res = None
        return res
    # end def get

    def put (self, path, what) :
        res = self.libcapi.OW_put (path, what, len (what))
        if res >= 0 :
            return True
        else :
            return False
    # end def put
# end class CAPI

### __END__ libcapi


