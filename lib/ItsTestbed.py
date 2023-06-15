"""ItsTestbed.py - A Distributed Testbed
NAME:
    ItsTestbed.py - A Distributed Testbed
"""

import os, sys, numbers, re
import ItsException, ItsServer, ItsReservationDatabase, ItsReservationLogger

class ItsTestbed ( object ):
    
    def __init__( self, cfg, baseDir ):
        self.cfg = cfg
        self.servers = []
        self.baseDir = baseDir
        self.reserveId = ""
        self.typeIndex = {}
        
    def makeServers ( self ):
        for spec in self.cfg.testbedCfg.yaml:
            self.servers.append( ItsServer.ItsServer( spec, self.baseDir ) )

    def checkAllServersSsh ( self ):
        for server in self.servers:
            print "CHECKING " + server.server
            out, rc = server.send( 'hostname' ).complete()
            if rc == 255 and re.search( 'WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!', out ):
                localhost = self.getServer( { 'type' : 'localhost' } )
                print "REPAIRING ITS SERVER KNOWN SSH HOSTS FOR: " + server.server
                out1, rc1 = localhost.sendCmd( 'ssh-keygen -f ~/.ssh/known_hosts -R ' + server.server ).complete()
                print out1
                print "RE-CHECKING " + server.server
                out2, rc2 = server.send( 'hostname' ).complete()
                if rc2 != 0:
                    raise ItsException.ItsServerSshConnectionException( "Testbed node still unresponsive to SSH: " + server.server )
            elif rc != 0:
                raise ItsException.ItsServerSshConnectionException( "Testbed node unresponsive to SSH: " + server.server )

    def validate ( self, args ):
        logger = ItsReservationLogger.ItsReservationLogger( self.cfg.harnessCfg )
        #db = ItsReservationDatabase.ItsReservationDatabase( self.cfg, args, logger )
        db = ItsReservationDatabase.ItsReservationDatabase()
        db.initialize( self.cfg )
        db.logger = logger        
        testbedsDir = os.path.join( db.reservationDir, 'reservations', 'testbeds' )
        # Looks like one of ours, don't check
        if self.cfg.testbedCfg.file.find( testbedsDir ) == 0:
            path, filename = os.path.split( self.cfg.testbedCfg.file )
            self.reserveId = os.path.splitext( filename )[0]
            return  # Does this let some through?
        if not db.isTestbedFree( self ):
            raise ItsException.ItsTestbedNotFree( "One or more testbed nodes is reserved." )

    def getServers( self, parameters ):
        matches = []
        # Lookup by index
        if 'server' in parameters and isinstance( parameters['server'], numbers.Integral ):
            matches.append( self.servers[parameters['server']] )
            return matches
        # Lookup by parameter matches
        for server in self.servers:
            #print server.toString();
            if self.serverMatches( parameters, server ):
                matches.append( server )
        if not matches:
            raise ItsException.ItsServerSpecNotFoundException( "Requested servers not found in testbed." )
        else:
            return matches
    
    def serverMatches ( self, parameters, server ):
        for key, value in parameters.items():
            #print key, value
            if server.__dict__.get( key ) != str( value ):
                return False
        return True

    def getServer( self, parameters ):
        matches = self.getServers( parameters )
        return matches[0]

    def getServerByIndex( self, index ):
        try:
            server = self.servers[index]
            return server
        except Exception as e:
            raise ItsException.ItsServerSpecNotFoundException( "Requested type not found in testbed config." )
    
    def getServerByIP(self, ip, parameters):
        for server in self.servers:
            if self.serverMatches(parameters, server ) and (ip in server.__dict__.get ( 'alternateIP' ) or ip == server.__dict__.get ('server')):
                return server
        raise ItsException.ItsServerSpecNotFoundException( "Requested server not found in testbed config." )
    
    def getNextServerByType( self, serverType ):
        servers = self.getServers( { 'type' : serverType } )
        if serverType in self.typeIndex and self.typeIndex[serverType] < len( servers ) - 1:        
            self.typeIndex[serverType] += 1
        else:
            self.typeIndex[serverType] = 0
        return servers[self.typeIndex[serverType]]
    
    def toString ( self ):
        s = ""
        for server in self.servers:
            s += server.toString()
            s += "=" * 50 + "\n"
        return s
    

    