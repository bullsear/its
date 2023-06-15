"""ItsCfg.py - Configuration
NAME:
    ItsCfg.py - Configuration
"""

import os, sys, yaml, uuid
import ItsException, ItsParameterCfg, ItsSuiteCfg, ItsTestbedCfg, ItsHarnessCfg

class ItsCfg ( object ):
    
    def __init__( self, arguments, baseDir ):
        self.arguments = arguments
        self.baseDir = os.path.realpath( baseDir )
        self.harnessCfg = ""
        self.parameterCfg = ""
        self.suiteCfg = ""
        self.suiteIsTempFile = False
        self.testFile = ""
        self.testbedCfg = ""
        self.testMapFile = ""
        self.testMap = ""
        os.environ['ITS_BASEDIR'] = baseDir
        self.pid = os.environ['ITS_PID'] = str( os.getpid() )
        
    def parseFiles( self ):
        self.harnessCfg = ItsHarnessCfg.ItsHarnessCfg( os.path.join( self.baseDir, 'cfg', 'harnesscfg', 'its.yaml' ) )
        self.harnessCfg.parseFile()
        self.harnessCfg.setEnv()
        
        if self.arguments.parametercfgfile != "":
            self.parameterCfg = ItsParameterCfg.ItsParameterCfg( self.arguments.parametercfgfile )
            self.parameterCfg.parseFile()
            self.parameterCfg.setEnv()
        
        if self.arguments.suitecfgfile != "":
            path, ext = os.path.splitext( self.arguments.suitecfgfile )
            if not ext == '.yaml':
                self.makeSuiteFile();
            self.suiteCfg = ItsSuiteCfg.ItsSuiteCfg( self.arguments.suitecfgfile )
            self.suiteCfg.parseFile()
        
        if self.arguments.testbedcfgfile != "":
            self.testbedCfg = ItsTestbedCfg.ItsTestbedCfg( self.arguments.testbedcfgfile )
            self.testbedCfg.parseFile()
    
    def cleanup ( self ):
        if self.suiteIsTempFile:
            os.remove( self.arguments.suitecfgfile )
    
    def makeSuiteFile( self ):
        self.suiteIsTempFile = True
        self.testFile = self.arguments.suitecfgfile
        c = " ".join( [ self.arguments.suitecfgfile, "-t", "$ITS_TESTBED" ] )
        testSpec = {
            'id' : '000',
            'command' : c,
        }
        filename = '/tmp/' + str( uuid.uuid4() ) + '.yaml'
        yaml.dump( [ testSpec ], file( filename, 'w' ), default_flow_style=False )
        self.arguments.suitecfgfile = filename
    
    def dumpEnv ( self ):
        s = ""
        for key in sorted( os.environ.keys() ):    # Ok
            value = os.environ.get( key )
            s += key + ": " + value + "\n"
        return s
    
    def toString( self ):
        s = ""
        s += "Harness Config:\n"
        s += self.harnessCfg.toString()
        if self.parameterCfg != "":
            s += "Parameter Config:\n"
            s += self.parameterCfg.toString()
        if self.suiteCfg != "":
            s += "Suite Config:\n"
            s += self.suiteCfg.toString()
        if self.testbedCfg != "":
            s += "Testbed Config:\n"
            s += self.testbedCfg.toString()
        return s
    
                
                