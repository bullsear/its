"""ItsTestSetup.py - Test Setup
NAME:
    ItsTestSetup.py - Test Setup
"""

import os, sys, re
import ItsTestArguments, ItsCfg, ItsTestbedCfg, ItsTestbed, ItsTime

class ItsTestSetup ( object ):
    
    def __init__( self ):
        ###baseDir = sys.argv[0]        # What?  Why did I do that?
        self.baseDir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )
        #print baseDir
        self.args = ItsTestArguments.ItsTestArguments()
        self.cfg = ItsCfg.ItsCfg( self.args, self.baseDir )
        self.cfg.testbedCfg = ItsTestbedCfg.ItsTestbedCfg( self.args.testbedcfgfile )
        self.cfg.testbedCfg.parseFile()
        self.testbed = ItsTestbed.ItsTestbed( self.cfg, self.baseDir )
        self.testbed.makeServers()
        self.time = ItsTime.ItsTime()
        self.batchStart = ""
        self.batchEnd = ""
    
    def getTestbed ( self ):
        return self.testbed
    
    def line1 ( self ):
        s = "-" * 65
        return s       
        
    def line2 ( self ):
        s = "=" * 65
        return s
    
    def start( self ):
        self.batchStart = self.time.dateTimeStamp()
        print self.line2()
        print "                          START TEST"
        print "                  " + self.batchStart
        print self.line2()
        
    def end ( self, check ):
        self.batchEnd = self.time.dateTimeStamp()        
        print self.line2()
        print "                    VERIFICATION SUMMARY"
        for r in check.all:
            print r
        print self.line2()
        print "                       FAILURE SUMMARY"
        for r in check.all:
            if re.search( "FAIL$", r ):
                print r
        print self.line2()
        print "                       RESULTS SUMMARY"
        print "                  " + self.batchEnd
        print "PASS: " + str( check.results['pass'] )
        print "FAIL: " + str( check.results['fail'] )
        print self.line2()
        self.exit_results( check )
        
    def exit_results ( self, check ):
        #global Results    
        
        if check.results['fail'] != 0:
            self.exit( "Some verifications FAILed", check.results['fail'] )
        else:
            if check.results['pass'] != 0:
                self.exit( "All verifications PASSed", 0 )
            else:
                self.exit( "No verifications recorded", 255 )        
        
    def exit ( self, comment, code ):
        print comment + "; exiting " + str( code ) + "..."
        sys.exit( code )        
        
        