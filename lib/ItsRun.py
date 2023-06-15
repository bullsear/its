"""ItsRun.py - An Its Run
NAME:
    ItsRun.py - An Its Run
"""

import os, sys, yaml

class ItsRun ( object ):
    
    def __init__( self, runner ):
        self.startTime = runner.startTime
        self.endTime = runner.endTime
        self.runId = runner.runId
        self.runDir = runner.runDir
        self.useremail = runner.cfg.arguments.email
        self.hostname = runner.hostname
        self.runURL = runner.runURL
        self.harnessPid = runner.pid
    
    def thaw ( self, filename ):
        yaml = yaml.load( file( filename, 'r' ) )

    def freeze ( self, log ):
        yaml.dump( self.__dict__, file( log, 'w' ), default_flow_style=False )
    
    