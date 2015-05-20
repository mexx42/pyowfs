# pyowfs
OWFS' (www.owfs.org) libowcapi wrapper for python using ctypes

This package provides one module with a thin wrapper around libowcapi (pyowfs/libcapi.py) and a 
slightly smarter wrapper around it (pyowfs/owfs.py) for easy access to the 1wire devices. 

It is inspired by the OWFS provided python bindings but, however is neither api 
compatible nor will it try to be in the future - at least i hope so ;)

One benefit over the OWFS provided python bindings is that you can access the memory of 
1wire devices even if there is a "\x00" in it ;) - that was the main reason i wrote this.

More information and a small introduction can be found at http://priesch.co.at/pyowfs.

Thanks for all ideas and collaborations !

regards,
marcus.
