"""ItsSuiteCfg.py - Test Case Suite Configuration
NAME:
    ItsSuiteCfg.py - Test Case Suite Configuration
"""

import os, sys, yaml, ItsException

class ItsSuiteCfg ( object ):
    
    def __init__( self, file ):
        self.file = os.path.realpath( file )
        self.yaml = None
    
    def parseFile ( self ):
        self.yaml = yaml.load( file( self.file, 'r' ) )
        self.validate()
        
    def validate( self ):
        if not self.yaml:
            raise ItsException.ItsUsageException( "No test specifications found in suite config: " + self.file )
    
    def toString ( self ):
        s = "File Path: " + self.file + "\n"        
        s += yaml.dump( self.yaml, default_flow_style=False, default_style='' )
        return s
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    