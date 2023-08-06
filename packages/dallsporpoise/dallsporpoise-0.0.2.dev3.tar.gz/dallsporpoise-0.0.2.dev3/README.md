Dall's Porpoise 
=========

dallsporpoise is another doppler oceanography library. 

It was originally forked and then cloned from lkilcher's [DOLFyN](http://lkilcher.github.io/dolfyn/). The motivation for a new package was dealing with corrupt data .VEC data files encountered in our 2019 Pilbara experiment.

I gave it a new name, rather than simply modify [DOLFyN](http://lkilcher.github.io/dolfyn/) as:

-  [DOLFyN](http://lkilcher.github.io/dolfyn/) is a very large package that handles many Doppler instruments in many setup modes, and does turbulence calculations
- I only wanted to be able to read our very large vector files from one particular experiment that were setup in one particular way. It was less effort to start from a stripped down package and build up, rather than try to properly integrate the changes I required within lkilcher's dolfyn.

The work here remains largely that of lkilcher, and so their license file is retained. Unless anyone is dealing with the specific file corruption that we encountered, I recommend using lkilcher's [DOLFyN](http://lkilcher.github.io/dolfyn/) instead. 

There are three subpackages within this package:

1. imp: For reading vector data
2. exp: Helps to stream vector data to NetCDF [if `stream=True' when reading vector]
3. lkd: this is basically lkilcher's [DOLFyN](http://lkilcher.github.io/dolfyn/) in all [most of] it's glory. Codes and directories with z_ in front are effectively 'commented out' [in as much that they won't be recognised by relative imports]. 

By keeping the lkd package as native, support code [e.g. code for coordinate rotations] can be used without dependency on Dolfyn. 

**NOTE: I have not bothered to copy over the vector IMU code as our vectors were on a fixed frame. Again, this library exists to get a very specific job done, it is not intended as a replacement for the MUCH MUCH more comprehensive [DOLFyN](http://lkilcher.github.io/dolfyn/).

**NOTE:  netCDF4, pandas and xarray are additional dependencies. 

**DOLfYN objects are presently still used.

Demo Data
=========

Sample data can be found in the [DOLFyN](http://lkilcher.github.io/dolfyn/) and [pIMOS](http://iosonobert.github.io/pIMOS/) packages. Relative imports from these packages will be found in the examples and notebooks folders. 

Tests
=====

There will be tests written for Dall's Porpoise, however there are none at present. Please use the tests in DOLFyN for now.


License
=======

Currently there is no license specific to DallsPorpoiseas this is a private repository. Please note as this was originally forked from lkilcher's DOLFyN, all files originating from that source are subject to DOLFyN's license (Apache License, Version 2.0).  

Version history
===============

v 0.0.0 Was basically dolfyn with a different VEC reader
v 0.1.0 Removed a lot of functions that I did not need and dramatically simplified the API. Dolfyn files have where possible been moved to the LKD subfolder. Files which are no longer needed are preceded with z_ and are ultimately intended for deletion. 