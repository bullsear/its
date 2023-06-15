"""ItsHarnessCfg.py - Harness Configuration
NAME:
    ItsHarnessCfg.py - Harness Configuration
"""

import os, sys, yaml
import ItsException

class ItsHarnessCfg ( object ):
    
    def __init__( self, file ):
        self.file = os.path.realpath( file )
        self.yaml = None
    
    def parseFile ( self ):
        self.yaml = yaml.load( file( self.file, 'r' ) )

    def setEnv ( self ):
        for key, value in self.yaml.items():
            os.environ[key] = str( value )
    
    def toString ( self ):
        s = "File Path: " + self.file + "\n"        
        s += yaml.dump( self.yaml, default_flow_style=False, default_style='' )
        return s
