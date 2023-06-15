#!/usr/bin/env python

"""trimlogs.py - Delete Old ITS Logs
NAME:
    trimlogs.py - Delete Old ITS Logs
    
SYNOPSIS:
    $> trimlogs.py

ARGUMENTS:

    N/A

DESCRIPTION:
    Designed to be run from cron, this deletes the oldest ITS logs if the directory gets
    too big.
    
DIRECTORY:
    The directory to be trimmed is defined with the ITS_LOGDIR variable in the its.yaml
    configuration file.

REFERENCE:
    https://www.youtube.com/watch?v=pq1SZrZbRMA        
"""
 
import os, sys, yaml, time, re, shutil, commands

if __name__ != '__main__':
    print __doc__
    os._exit(0)
    
# Where are we (pwd)?
baseDir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )
sys.path.append( os.path.join( baseDir, 'lib' ) )

import ItsHarnessCfg

# Parse the configs 
harnessCfg = ItsHarnessCfg.ItsHarnessCfg( os.path.join( baseDir, 'cfg', 'harnesscfg', 'its.yaml' ) )
harnessCfg.parseFile()

logDir = harnessCfg.yaml['ITS_LOGDIR']
maxSize = harnessCfg.yaml['ITS_MAXLOGDIRSIZE']

now = time.time()

regex = re.compile( '^\d+\.' )

def rmDir( directories ):
    d = directories.pop()
    if regex.match( d ):        
        path = os.path.join( logDir, d )        
        if os.path.isdir( path ):
            print "Removing directory: " + path
            shutil.rmtree( path )

directories = sorted( os.listdir( logDir ), reverse=True )

while True:
    size = commands.getoutput( 'du -bs ' + logDir ).split()[0]
    print size
    if int( size ) < int( maxSize ):
        break
    else:
        rmDir( directories )

















