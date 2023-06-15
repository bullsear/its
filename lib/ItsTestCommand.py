"""ItsTestCommand.py - A Command
NAME:
    ItsTestCommand.py - A Command
"""

import os, sys, subprocess
import ItsException, ItsTime

class ItsTestCommand ( object ):
    
    def __init__( self, command, server, baseDir, scpfrom='', scpto='', verbose=2 ):
        self.command = command
        self.server = server
        self.baseDir = baseDir
        self.sshscript = os.path.join( self.baseDir, 'bin', 'ssh.bash' )
        self.scpscript = os.path.join( self.baseDir, 'bin', 'scp.bash' )
        self.scpfrom = scpfrom
        self.scpto = scpto
        self.proc = ""
        self.time = ItsTime.ItsTime()
        self.pid = ""
        self.stdout = ""
        self.rc = ""
        self.verbose = verbose

    def getCommand ( self ):
        harnessPid = os.environ.get('ITS_PID')
        # We're Running inside the harness
        if os.environ.get('ITS_TESTLOGDIR'):
            harnessPid = self.getHarnessPid()
        command = " ".join( [ self.sshscript, harnessPid, self.server.username, self.server.password, self.server.server, "\'" + self.command + "\'" ] )
        return command
    
    def getHarnessPid ( self ):
        path = os.path.join( os.environ.get('ITS_TESTLOGDIR'), '..', 'pid.log' )
        handle = open( path, 'r' )
        pid = handle.read()
        handle.close
        return pid
    
    def send ( self ):
        if len( self.scpfrom ) and len( self.scpto ):
            return self.sendCmd( self.getScpCommand() )
        else:
            return self.sendCmd( self.getCommand() )
    
    def sendCmd ( self, command ):
        self.proc = subprocess.Popen(
            command,
            shell = True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.pid = str( self.proc.pid )
        self.showStart()
        return self
    
    # def send ( self ):
    #     #print self.getCommand()
    #     
    #     self.proc = subprocess.Popen(
    #         self.getCommand(),
    #         shell = True,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT,
    #     )
    #     self.pid = str( self.proc.pid )
    #     self.showStart()
    #     return self
    
    def getScpCommand ( self ):
        command = " ".join( [ self.scpscript, self.server.username, self.server.password, self.server.server, self.scpfrom, self.scpto ] )
        return command

    def scp ( self ):
        #print self.getCommand()
        
        self.proc = subprocess.Popen(
            self.getScpCommand(),
            shell = True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.pid = str( self.proc.pid )
        self.showStart()
        return self

    def complete ( self ):
        stdout, rc = self.stream()
        return stdout.rstrip(), rc
    
    def showEnd ( self ):
        if self.verbose == 0:
            return        
        end = [
            self.time.dateTimeStamp(),
            "EXITCODE",
            "[" + self.pid + "]",
            str( self.rc ),
        ]
        print " ".join( end )
    
    def showStart ( self ):
        if self.verbose == 0:
            return        
        start = [
            self.time.dateTimeStamp(),
            "SEND    ",
            "[" + self.pid + "]",
            "(" + self.server.server + ")",
            "\"" + self.command + "\"",
        ]
        print " ".join( start )
    
    def showOut ( self ):
        out = [
            self.time.dateTimeStamp(),
            "OUTPUT  ",
            "[" + self.pid + "]",
        ]
    
    def line1 ( self ):
        s = "-" * 65
        return s       
    
    def stream ( self ):
        stdout = ""
        self.showOut()
        while True:
            line = self.proc.stdout.readline()
            if line != "":
                if self.verbose != 0:
                    print "   " + line,
                stdout += line
            else:
                break
        self.proc.wait()
        self.rc = self.proc.returncode
        self.showEnd()
        return stdout, self.rc
    
