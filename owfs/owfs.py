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
#    owfs
#
# Purpose
#    high-level owfs functionality based on libcapi
#
# Revision Dates
#    22-Dec-2009 (MP) Creation
#    ««revision-date»»···
#--
import libcapi
import re

sensor_rex = re.compile ("[0-9A-F]{2}.[0-9A-F]{12}/")

class Dir (object) :
    def __init__ (self, path, capi) :
        self._path   = path
        self.capi = capi
        self.cached  = True
    # end def __init__

    def __repr__ (self) :
        return "<Dir %r>" % self.path
    # end def __repr__

    @property
    def path (self) :
        if not self.cached :
            return "/uncached" + self._path
        else :
            return self._path
    # end def path

    def use_cache (self, yesno) :
        self.cached = bool (yesno)
    # end def use_cache

    def iter_entries (self) :
        """iterates over all the enries."""
        for e in self.capi.get (self.path).split (",") :
            if not sensor_rex.match (e) :
                if e.endswith ("/") :
                    yield Dir (self.path + e, self.capi)
                else :
                    yield e
    # end def iter_entries

    def get (self, key) :
        for e in self.iter_entries () :
            if isinstance (e, Dir) :
                basename = e.path[:-1].split ("/") [-1]
                if key == basename :
                    return e
            else :
                basename = e.split ("/") [-1]
                if key == basename :
                    return self.capi.get ("%s%s" % (self.path, e))
        raise KeyError (key)
    # end def get

    def has_key (self, key) :
        return key in self.capi.get (self.path).split (",")
    # end def has_key
# end class Dir

class Sensor (Dir) :
    def __init__ (self, path, capi) :
        self._path   = path
        self.capi = capi
        self.cached  = True
    # end def __init__

    def __repr__ (self) :
        return "<Sensor %r>" % (self.path)
    # end def __repr__

    def iter_sensors (self) :
        for e in self.capi.get (self.path).split (",") :
            if sensor_rex.match (e) :
                yield Sensor ("%s%s" % (self.path, e), self.capi)
    # end def iter_sensors

    def find (self, **kw) :
        res = []
        for sensor in self.iter_sensors () :
            failed = False
            for k, v in kw.iteritems () :
                if not sensor.has_key (k) :
                    failed = True
                elif sensor.get (k) != v :
                    failed = True
            if not failed :
                res.append (sensor)

            res.extend (sensor.find (**kw))
        return res
    # end def find

# end class Sensor

class Connection (Sensor) :
    def __init__ (self, port) :
        capi = libcapi.CAPI ()
        capi.init (port)
        super (Connection, self).__init__ ("/", capi)
    # end def __init__
# end class Connection

### __END__ owfs


