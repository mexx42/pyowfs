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
#    22-Dec-2009 (MPH) Creation
#    ««revision-date»»···
#--
import libcapi
import re

sensor_rex = re.compile ("[0-9A-F]{2}.[0-9A-F]{12}/")

class Dir (object) :
    """Represent a directory node in the owfs hierarchy
    """
    def __init__ (self, path, capi) :
        self._path  = path
        self.capi   = capi
        self.cached = True
    # end def __init__

    def __repr__ (self) :
        return "<Dir %r>" % self.path
    # end def __repr__

    @property
    def path (self) :
        """Returns the absolute path in the owfs hierarchy with prepended
        '/uncached' if caching is turned off.
        """
        if not self.cached :
            return "/uncached" + self._path
        else :
            return self._path
    # end def path

    def use_cache (self, yesno) :
        """Turn caching on/off
        """
        self.cached = bool (yesno)
    # end def use_cache

    def iter_entries (self) :
        """Iterates over all entries under this directory node.
        """
        for e in self.capi.get (self.path).split (",") :
            if not sensor_rex.match (e) :
                if e.endswith ("/") :
                    yield Dir (self.path + e, self.capi)
                else :
                    yield e
    # end def iter_entries

    def get (self, key) :
        """Get a given entry.

        Basically this resembles a read access to self.path/key.
        """
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

    def put (self, key, value) :
        """Write a given entry.

        This resembles a write access to self.path/key.
        """
        if self.has_key (key) and not isinstance (self.get (key), Dir) :
            val = str (value)
            return self.capi.put ("%s%s" % (self.path, key), val)
    # end def put

    def has_key (self, key) :
        return key in self.capi.get (self.path).split (",")
    # end def has_key
# end class Dir

class Sensor (Dir) :
    """Represents any kind of owfs sensor.

    Basically the same as 'Dir' but has additional methods 'iter_sensors' to
    iterate over it's child sensors (e.g. DS2409) and 'find' to find other
    sensors by matching keyword arguments.
    """
    def __init__ (self, path, capi) :
        self._path   = path
        self.capi = capi
        self.cached  = True
    # end def __init__

    def __repr__ (self) :
        return "<Sensor %s - %s>" % (self.path, self.get ("type"))
    # end def __repr__

    def iter_sensors (self) :
        """Iterates over all 'sensors' which can be found.

        'sensors' are identified by the special representation in the owfs
        hierarchy: '[0-9A-F]{2}.[0-9A-F]{12}/' (e.g. 12.E8F672000000)
        """
        for e in self.capi.get (self.path).split (",") :
            if sensor_rex.match (e) :
                yield Sensor ("%s%s" % (self.path, e), self.capi)
    # end def iter_sensors

    def find (self, **kw) :
        """Recursively searches for sensors matching the given criteria.

        returns a list of sensors - even if only one is found.

        example:
        >>> c = owfs.Connection ("192.168.2.112:3030")
        >>> s = c.find (type="DS2406") [0]
        >>> s
        <Sensor '/12.E8F672000000/'>
        >>> s.get ("type")
        'DS2406'

        The 'type' specified on the find call is the attribute that is
        matched during the search with the value "DS2406" which matches to
        exactly one sensor which has an attribute "type" with a value of
        "DS2406". This way you can search by any attribute you like. Note
        that if you specify more than one attribute *all* attributes must be
        present (logical AND).

        """
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
    """This is the 'root' sensor of your owfs hierarchy.

    It initialises libcapi and connects to the port you specify. For port
    specifications look at the owfs documentation. Examples for valid port's
    are: '192.168.2.112:3030', 'u'.

    typical usage :

    >>> from pyowfs import Connection
    >>> root = Connection ("192.168.2.112:3030")
    >>> for s in root.find () : print s
    ...
    <Sensor /20.C1A00B000000/ - DS2450>
    <Sensor /12.E8F672000000/ - DS2406>
    <Sensor /29.336C08000000/ - DS2408>

    disabling the cache is reflected in the %r of the sensor :

    >>> s.use_cache (0)
    >>> for s in root.find () : print s
    ...
    <Sensor /uncached/20.C1A00B000000/ - DS2450>
    <Sensor /uncached/12.E8F672000000/ - DS2406>
    <Sensor /uncached/29.336C08000000/ - DS2408>

    find sensors of a specific type :

    >>> s = root.find (type="DS2406") [0]

    dump all entries of the sensor :

    >>> for e in s.iter_entries () : print e
    ...
    PIO.BYTE
    PIO.ALL
    PIO.A
    PIO.B
    <Dir '/12.E8F672000000/T8A/'>
    <Dir '/12.E8F672000000/TAI8570/'>
    address
    alias
    channels
    crc8
    family
    flipflop.BYTE
    flipflop.ALL
    flipflop.A
    flipflop.B
    id
    latch.BYTE
    latch.ALL
    latch.A
    latch.B
    locator
    memory
    <Dir '/12.E8F672000000/pages/'>
    power
    present
    r_address
    r_id
    r_locator
    sensed.BYTE
    sensed.ALL
    sensed.A
    sensed.B
    set_alarm
    type

    access 'memory' :

    >>> s.get ("memory")
    "h\xaa\xaa\x1d\xc6\x84|\xcd\xa1;P\9d3\xd5\x91" ...

    'pages' is a directory, so lets see whats beneath it :

    >>> s.get ("pages")
    <Dir '/12.E8F672000000/pages/'>
    >>> for e in s.get ("pages").iter_entries () : print e
    ...
    page.ALL
    page.0
    page.1
    page.2
    page.3

    access to individual pages :

    >>> s.get ("pages").get ("page.1")
    '\xff\x00\x8b\xa3J\r\x1e\x84\xcd\x90\x15:\x9d' ...
    >>> s.get ("pages").get ("page.2")
    '\xb1k-\x0bQ\x04\xe7\xdfh\xa1\d\xc6\x84|\xcd2' ...

    also possible to access long paths directly via underlying libowcapi :

    >>> root.capi.get ("/bus.0/interface/settings/usb/datasampleoffset")
    '           8'
    >>> root.capi.put ("/bus.0/interface/settings/usb/datasampleoffset", "10")
    True
    >>> root.capi.get ("/bus.0/interface/settings/usb/datasampleoffset")
    '          10'

    """

    def __init__ (self, port) :
        capi = libcapi.CAPI ()
        capi.init (port)
        super (Connection, self).__init__ ("/", capi)
    # end def __init__
# end class Connection

### __END__ owfs
