#!/usr/bin/env python

"""selenium_import.py - Wrap an Exported Selenium Script
NAME:
    selenium_import.py - Wrap an Exported Selenium Script

SYNOPSIS:
    $> selenium_import.py -f <firefoxscript> -r <browser> | tee <newscript>

ARGUMENTS:

    -f = Path to a Python script exported by the Firefox Selenium Plug-in
    -r = The browser to test (chrome|firefox)

DESCRIPTION:
    Firefox has a Selenium record and playback plugin that creates a test.  The test
    can be exported as a python script.  This script turns that script into
    a portable test script suitable for ITS reservations and execution.
    
"""

import sys, getopt, re

filePath = ''
showHelp = False
driver = ''

sys.argv.pop( 0 )

try:
    opts, args = getopt.getopt( sys.argv, "f:r:h" )
except getopt.GetoptError:
    print "USAGE ERROR: Incorrect command line options (its -h for help)"
    sys.exit(2)

for opt, arg in opts:
    if opt in ( "-h" ):
        showHelp = True   
    elif opt in ( "-f" ):
        filePath = arg
    elif opt in ( "-r" ):
        driver = arg

#print file
### Need to check for arguments here

if showHelp:
    print __doc__
    sys.exit(2)

if not len( filePath ) or not len( driver ):
    print "USAGE ERROR: Incorrect command line options (its -h for help)"
    sys.exit(2)

def header():
    header = """\
#!/usr/bin/env python

import os, sys, gc
import ItsTestSetup

testbed = ItsTestSetup.ItsTestSetup().getTestbed()

linuxwebserver = testbed.getServer( { 'type' : 'linuxwebserver' } )
windowswebclient = testbed.getServer( { 'type' : 'windowswebclient' } )
"""
    print header

def constructor():
    start = '''        self.selenium = selenium( windowswebclient.server, 4444, "*'''
    end = '''", "http://" + linuxwebserver.server )'''
    return ''.join( [ start, driver, end ] )

def readLineFile():
    matchString = re.compile( r'        self.selenium = selenium' )
    f = open( filePath, 'r' )
    while True:
        line = f.readline()
        if not line:
            break
        if matchString.match( line ):
            print constructor()
        else:
            print line,
    print "\n"
    f.close

header()
readLineFile()
    
