"""ItsServer.py - An SSH Server
NAME:
    ItsServer.py - An SSH Server
"""

import os, sys
import ItsException, ItsTime, ItsTestCommand

class ItsServer ( object ):
    
    def __init__( self, spec, baseDir, verbose=2 ):
        for key, value in spec.items():
            self.__dict__[key] = value
        self.baseDir = baseDir
        self.verbose = verbose

    #    self.ssh = paramiko.SSHClient()
    #    self.ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    #    self.time = ItsTime.ItsTime()
    #    
    #def connect ( self ):
    #    try:
    #        self.ssh.connect( self.server, username=self.username, password=self.password )
    #    except paramiko.SSHException, exception:
    #        self.sys.stderr.write( "SSH CONNECTION EXCEPTION: " + str( exception ) )
    #        sys.exit( 1 )
    #
    #def cmd ( self, command ):
    #    command += " 2>&1"
    #    stdin, stdout, stderr = self.ssh.exec_command( command, bufsize=0 )
    #    line = None
    #    while 1:
    #        line = None
    #        try:
    #            line = stdout.next()
    #        except Exception:
    #            break
    #        print self.time.dateTimeStamp() + ": " + line,
    
    #def cmd ( self, command ):
    #    
    #    command += " 2>&1"
    #    
    #    test.proc = subprocess.Popen(
    #        command,
    #        shell = True
    #    )
    #    
    #    test.pid = test.proc.pid
    #    test.writeMeta()
    #    
    #    # Blocking tests end here
    #    if test.background != "1":
    #        test.proc.wait()
    #        test.rc = test.proc.returncode
    #        self.testResult( test )
      
    def send ( self, command ):
        
        cmd = ItsTestCommand.ItsTestCommand( command, self, self.baseDir, verbose=self.verbose )
        
        cmd.send()
        
        return cmd
    
    def sendCmd ( self, command ):
        
        cmd = ItsTestCommand.ItsTestCommand( command, self, self.baseDir, verbose=self.verbose )
        
        cmd.sendCmd( command )
        
        return cmd
        
    #def sendWait ( self, command ):
    #    
    #    cmd = ItsTestCommand.ItsTestCommand( command, self, self.baseDir )
    #
    #    cmd.send( True )
    #    
    #    return cmd
    #    
    #def sendBg ( self, command ):
    #    
    #    cmd = ItsTestCommand.ItsTestCommand( command, self, self.baseDir )
    #
    #    cmd.send( False )
    #
    #    return cmd
    
    def toString ( self ):
        s = ""
        for key, value in self.__dict__.items():
            if key in ['ssh','time']:
                continue
            s += key + ": " + value + "\n"
        return s
    
