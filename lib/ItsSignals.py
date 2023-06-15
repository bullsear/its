"""ItsSignals.py - Signal Handling
NAME:
    ItsSignals.py - Signal Handling
"""

import os, sys, socket, time, signal
import ItsTestBuilder, ItsException, ItsRunner, ItsLogger

class ItsSignals ( object ):
    
    def __init__( self, runner ):
        self.runner = runner
        self.logger = ""
        
    def register ( self ):
        signal.signal( signal.SIGINT, self.handle_cntl_c )
        
    def handle_cntl_c( self, signal, frame ):
        #print "HANDLING CNTL-C"
        print
        self.logger.write( "HANDLING CNTL-C", "" )
        #self.runner.killAllTests( self.runner.testSuite.getRunningTests() )
        self.runner.killAllTests( self.runner.testSuite.tests )
        self.runner.endBatch()
        sys.exit(255)
        
        
