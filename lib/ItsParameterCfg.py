"""ItsParameterCfg.py - Global Its Environment Variable Configuration
NAME:
    ItsParameterCfg.py - Global Its Environment Variables Configuration
"""

import os, sys, yaml, ItsException

class ItsParameterCfg ( object ):
    def __init__ ( self, file ):
        self.file = os.path.realpath( file )
        self.yaml = None
    
    def parseFile ( self ):
        self.yaml = yaml.load( file( self.file, 'r' ) )
        
    def setEnv ( self ):
        os.environ['PYTHONUNBUFFERED'] = '1'
        for key, value in self.yaml.items():
            os.environ[key] = value
    
    def toString ( self ):
        s = "File Path: " + self.file + "\n"
        s += yaml.dump( self.yaml, default_flow_style=False, default_style='' )
        return s
    
    
