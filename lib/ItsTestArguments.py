"""ItsTestArguments.py - Test Script Arguments
NAME:
    ItsTestArguments.py - Test Script Arguments
"""

import os, sys, getopt, ItsException
import __main__ as main

class ItsTestArguments ( object ):
    
    def __init__ ( self ):
        self.scriptname = sys.argv[0]

        self.testbedcfgfile = os.environ.get( 'ITS_TESTBED' )      # -t : The testbed config file
        self.command = ""                                          # -c : A one-shot command for easicli
        self.verbose = 2                                           # -v : How much output to show
        
        if self.testbedcfgfile is None:
            #self.scriptname = sys.argv.pop()
            myArgs = sys.argv
            myArgs.pop(0)
            
            try:
                opts, args = getopt.getopt( myArgs, "t:c:v:" )
                #print opts, args
            except getopt.GetoptError:
                print "USAGE ERROR: Incorrect command line options"
                #print "YOUR COMMAND: " + self.scriptname + " " + " ".join( sys.argv )            
                sys.exit(2)
                
            for opt, arg in opts:
                #print opt, arg
                if opt in ( "-t" ):
                    self.testbedcfgfile = arg
                elif opt in ( "-c" ):
                    self.command = arg
                elif opt in ( "-v" ):
                    self.verbose = arg
            
            try:
                self.checkArgs()
            except ItsException.ItsUsageException as e:
                print "USAGE ERROR: ",
                print e
                print "YOUR COMMAND: " + " ".join( sys.argv )
                #print main.__doc__
                sys.exit( 255 )
                
        #else:
        #    self.scriptname = sys.argv.pop()
            
    def checkArgs ( self ):
                
        if self.testbedcfgfile == "":
            raise ItsException.ItsUsageException( "Missing/incorrect usage argument(s)." )
        
        if not os.path.isfile( str( self.testbedcfgfile ) ):
            raise ItsException.ItsUsageException( "Missing testbed config file(s) argument or ENV variable." )
        
        if os.path.basename( self.testbedcfgfile ) == "EXAMPLE.yaml":
            raise ItsException.ItsUsageException( "Using EXAMPLE.yaml config files prohibited." )
        
    def toString ( self ):
        s = "=" * 65 + "\n"
        s += "                           ARGUMENTS\n"        
        s += "Testbed Config File:   " + str( self.testbedcfgfile ) + "\n"
        s += "Command:               " + self.command + "\n"
        s += "=" * 65 + "\n"
        return s        
        
        