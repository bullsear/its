"""ItsTest.py - Test Case 
NAME:
    ItsTest.py - Test Case 
"""

import os, sys, yaml, time, datetime, re, string, threading
import ItsException, ItsTime, ItsCLIParser

class ItsTest ( object ):
    
    def __init__( self, spec, ordinal, server, serverId, instanceId, runDir, baseDir, cfg, loops, runner ):
        #print spec
        self.runner = runner
        self.cfg = cfg
        self.loops = loops
        self.stream = 1
        self.id = ""
        self.command = ""
        self.count = 1
        self.background = 0
        self.presleep = ".000001"   # Assure [epoch] is unique
        self.postsleep = ""
        self.wait = ""
        self.ignore = 0
        self.type = ""        
        self.baseDir = baseDir
        self.haltonfail = 0
        self.scpfrom = ""
        self.scpto = ""
        self.name = ""
        self.timeout = ""
        for key, value in spec.items():
            self.__dict__[key] = str( value )
        if 'wait' in spec and isinstance( spec['wait'], list ):
            self.wait = []
            for id in spec['wait']:
                self.wait.append( id )
        self.ordinal = ordinal
        self.server = server
        self.serverId = str( serverId )
        self.instanceId = str( instanceId )
        self.runDir = runDir
        self.logDir = ""
        self.log = ""
        self.sshscript = os.path.join( self.baseDir, 'bin', 'ssh.bash' )
        self.scpscript = os.path.join( self.baseDir, 'bin', 'scp.bash' )
        self.proc = ""
        self.pid = ""
        self.rc = ""
        self.meta = ""
        self.result = ""
        self.env = ""
        self.testInstanceId = ""
        self.startTime = ""
        self.endTime = ""
        self.interpolated = False
        self.time = ItsTime.ItsTime()
        self.timer = ""
        self.ended = False
        self.duration = ""
        self.parser = ItsCLIParser.ItsCLIParser()
        
    def setLogDir ( self, runDir ):
                
        if self.name == "":
                    
            commandStub = self.command
                    
            # An scp command
            if self.scpfrom != "":
                commandStub = 'scp'
                
            # A CLI command
            else: 
                # It's a compound statement; get the last one
                if re.search( ';', commandStub ):      
                    commandStub = re.sub( '.+; *', '', commandStub )
                    
                commandStub = commandStub.split( " " )[0]           # Get the first token
                commandStub = os.path.basename( commandStub )       # Get the basename
                commandStub, ext = os.path.splitext( commandStub )  # Remove the extension
                commandStub = commandStub.split( " " )[0][:8]       # Truncate to 8 characters

            self.name = commandStub
        
        self.setTestInstanceId()
              
        self.logDir = os.path.join( runDir, self.testInstanceId )
        
        self.log = os.path.join( self.logDir, 'output.log' )
        self.meta = os.path.join( self.logDir, 'meta.log' )
        self.env = os.path.join( self.logDir, 'environment.txt' )
        
        os.makedirs( self.logDir )
    
    def setTestInstanceId ( self ):
        if isinstance( self.server, basestring ):
            self.testInstanceId = "_".join( [ str( self.ordinal ).zfill( 6 ), "none", self.name, self.id ] )
        else:
            self.testInstanceId = "_".join( [ str( self.ordinal ).zfill( 6 ), self.server.server, self.name, self.id ] )
            
    def getCommand ( self ):
        
        if not self.interpolated:
            self.interpolate()
            self.interpolated = True
        
        server = ""
        if not isinstance( self.server, basestring ):
            server = self.server.server
        
        if server != "":
            if self.scpfrom == "":
                harnessPid = os.environ.get('ITS_PID')
                command = " ".join( [ self.sshscript, harnessPid, self.server.username, self.server.password, self.server.server, "\"" + self.command + "\"", " > ", self.log ] )
            else:     
                command = " ".join( [ self.scpscript, self.server.username, self.server.password, self.server.server, self.scpfrom, self.scpto, " > ", self.log ] )
        else:
            command = " ".join( [ self.command, " > ", self.log, "2>&1" ] )
                    
        return command    
    
    def interpolate ( self ):        
        
        command = self.command
        
        epoch = self.time.getHighResolutionEpoch()
        
        server = ""
        if not isinstance( self.server, basestring ):
            server = self.server.server
        
        command = command.replace( '[server]', server )                         # the server name
        command = command.replace( '[ordinal]', str( self.ordinal ) )           # the unique execution ordinal id
        command = command.replace( '[instanceId]', str( self.instanceId ) )     # the count id on a server 
        command = command.replace( '[id]', str( self.id ) )                     # the test database id
        command = command.replace( '[testInstanceId]', self.testInstanceId )    # the string that gets logged
        command = command.replace( '[epoch]', str( epoch ) )                    # epoch seconds    
        
        # User defined loop lists (all combinations)
        if self.loops:
            for key in sorted( self.loops ):
                command = command.replace( '[' + key + ']', str( self.loops[key] ) ) 
        self.command = command
        
    def postSleep ( self ):
        if self.postsleep.decode( 'utf-8' ).isnumeric():
            time.sleep( float( self.postsleep ) )     
    
    def writeMeta ( self ):
        if self.cfg.arguments.verbose > 1:
            obj = self
        else:
            server = ""
            type = ""
            if not isinstance( self.server, basestring ):
                server = self.server.server
                type = self.server.server
            obj = {
                'name' : self.name,
                'background' : self.background,
                'command' : self.getCommand(),
                'count' : self.count,
                'endTime' : self.endTime,
                'id' : self.id,
                'ignore' : self.ignore,
                'instanceId' : self.instanceId,
                'logDir' : self.logDir,
                'loops' : self.loops,
                'ordinal' : self.ordinal,
                'pid' : self.pid,
                'presleep' : self.presleep,
                'postsleep' : self.postsleep,
                'rc' : self.rc,
                'result' : self.result,
                'server' : server,
                'startTime' : self.startTime,
                'stream' : self.stream,
                'testInstanceId' : self.testInstanceId,
                'type' : type,
                'wait' : self.wait,
                'haltonfail' : self.haltonfail,
                'timeout' : self.timeout,
                'duration' : self.duration,
            }
        yaml.dump( obj, file( self.meta, 'w' ), default_flow_style=False )
    
    def initialize ( self, rundir, logger ):
        self.setLogDir( rundir )
        self.setEnv()
        self.markStart( logger )
        
    def markStart ( self, logger ):
        self.startTime = logger.write( "START", self.testInstanceId )
        self.writeMeta()

    def markEnd ( self, logger ):
        if self.ended:
            return
        self.ended = True
        self.endTime = logger.write( "END", self.testInstanceId + " " + str( self.result ) )
        self.computeDuration()
        self.writeMeta()       
    
    def computeDuration ( self ):
        if len( self.startTime ) and len( self.endTime ):
            start = self.dateTime( self.startTime )
            end = self.dateTime( self.endTime )
            delta = end - start
            duration = delta.days * 86400 + delta.seconds
            self.duration = str( duration ) + '.' + str( delta.microseconds )
                
    def dateTime ( self, timeString ):
        return datetime.datetime.strptime( timeString, '%Y-%m-%d %H:%M:%S.%f' )
    
    def setEnv ( self ):
        os.environ['ITS_INSTANCEID'] = str( self.testInstanceId )
        os.environ['ITS_TESTLOGDIR'] = str( self.logDir )
        os.environ['ITS_TESTLOG'] = str( self.log )
        handle = open( self.env, 'w' )
        handle.write( self.cfg.dumpEnv() )
        handle.close
        
    def isRunning ( self ):
        if self.proc != "" and self.proc.poll() is not None:
            return True
        else:
            return False
                    
    def toString( self ):
        s = ""
        for key, value in self.__dict__.items():
            if key == 'server':
                continue
            s += key + ": " + str( value ) + "\n"
        s += self.server.toString()
        return s
        
    