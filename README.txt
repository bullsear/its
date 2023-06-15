README
======

This is the root directory of the ITS test harness.  The files here are
version controlled.  Do not make changes to anything in this directory.  If
you do, your changes will be automatically erased with the next update of ITS.

What's here:

bin/    - This directory contains the its.py harness and other scripts
lib/    - This directory contains the libraries used by its.py
cfg/
    harnesscfg/its.yaml       - This is the global its config file; don't edit this
    suitecfg/EXAMPLE.yaml     - This is a sample suite config file
    parametercfg/EXAMPLE.yaml - This is a sample optional, user-defined parameter config file
    testbedcfg/EXAMPLE.yaml   - This is a sample testbed config file
clientutils/   - This directory contains client utility scripts

To get started with ITS, first watch the video,

    https://www.youtube.com/watch?v=pq1SZrZbRMA

read the docs,

   ./its.py -h

then try a run:

    ./its.py -a run -u <firstname.lastname> -t ../cfg/testbedcfg/tryme.yaml -s ../cfg/suitecfg/tryme.yaml


