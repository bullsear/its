"""ItsTestbedCfg.py - Testbed Configuration
NAME:
    ItsTestbedCfg.py - Testbed Configuration
"""

import os, sys, yaml
import ItsException, ItsServer

class ItsTestbedCfg ( object ):
    
    def __init__( self, file ):
        self.file = os.path.realpath( file )
        self.basename = os.path.basename( self.file )
        self.yaml = None
    
    def parseFile ( self ):
        self.yaml = yaml.load( file( self.file, 'r' ) )
    
    def toString ( self ):
        s = "File Path: " + self.file + "\n"
        s += yaml.dump( self.yaml, default_flow_style=False, default_style='' )
        return s
