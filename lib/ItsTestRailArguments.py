"""ItsTestRailArguments.py - Arguments for Testrail Results Upload Script
NAME:
    ItsTestRailArguments.py - Arguments for Testrail Results Upload Script
    
    ./testrail_results.py -i 614 -d /var/log/its/1469569601.whit7-10.hgst.com -u <email> -p <password>
"""

import os, sys, yaml, getopt
import ItsException

class ItsTestRailArguments ():
    
    def __init__( self ):
        self.testrailRunId = ''
        self.runDir = ''
        self.verbose = 0
        self.user = ''
        self.password = ''
        self.help = False
        
        myArgs = sys.argv
        myArgs.pop(0)        

        try:
            opts, args = getopt.getopt( myArgs, "i:d:v:u:p:h" )
            #print opts, args
        except getopt.GetoptError:
            print "USAGE ERROR: Incorrect command line options"
            #print "YOUR COMMAND: " + self.scriptname + " " + " ".join( sys.argv )            
            sys.exit(2)        
        
        for opt, arg in opts:
            #print opt, arg
            if opt in ( "-i" ):
                self.testrailRunId = arg
            elif opt in ( "-d" ):
                self.runDir = arg
            elif opt in ( "-v" ):
                self.verbose = arg
            elif opt in ( "-u" ):
                self.user = arg             # Usually an email address
            elif opt in ( "-p" ):
                self.password = arg
            elif opt in ( "-h" ):
                self.help = True
        
    def checkArgs ( self ):
        if self.testrailRunId == "":
            raise ItsException.ItsUsageException( "Missing Testrail run id argument(s)." )
        if self.runDir == "":
            raise ItsException.ItsUsageException( "Missing ITS run directory argument(s)" )
        if not os.path.isdir( self.runDir ):
            raise ItsException.ItsUsageException( "ITS run directory doesn't exist" )
        if self.user == "":
            raise ItsException.ItsUsageException( "Missing Testrail username, usually an email address" )            
        if self.password == "":
            raise ItsException.ItsUsageException( "Missing Testrail password" )            
            
    def toString ( self ):
        s = "=" * 65 + "\n"
        s += "                           ARGUMENTS\n"        
        s += "Testrail Run Id:     " + str( self.testrailRunId ) + "\n"
        s += "ITS Run Directory:   " + self.runDir + "\n"
        s += "Verbosity:           " + str( self.verbose ) + "\n"
        s += "Username (email):    " + str( self.user ) + "\n"
        s += "Password:            " + str( self.password ) + "\n"
        s += "=" * 65 + "\n"
        return s        
        