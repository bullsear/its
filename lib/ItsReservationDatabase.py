"""ItsReservationDatabase.py - Reservations Host Database
NAME:
    ItsReservationDatabase.py - Reservations Host Database
"""

import os, sys, yaml, re, copy, errno
import ItsException, ItsReservation

class ItsReservationDatabase ( object ):
    
    #def __init__( self, cfg, args, logger ):
    def __init__( self ):
        #self.cfg = cfg
        self.cfg = ""
        #self.harnessCfg = cfg.harnessCfg
        self.harnessCfg = ""
        ###self.args = args
        self.args = ""
        ###self.logger = logger
        self.logger = ""
        #self.reservationDir = self.harnessCfg.yaml['ITS_RESERVATION_DIR']
        self.reservationDir = ""
        #self.poolsDir = os.path.join( self.reservationDir, 'pools' )
        self.poolsDir = ""
        #self.typesDir = os.path.join( self.reservationDir, 'types' )
        self.typesDir = ""
        #self.activeReservationsDir = os.path.join( self.reservationDir, 'reservations' )
        self.activeReservationsDir = ""
        #self.activeReservationsHostsDir = os.path.join( self.activeReservationsDir, 'hosts' )
        self.activeReservationsHostsDir = ""
        #self.activeReservationsTestbedsDir = os.path.join( self.activeReservationsDir, 'testbeds' )
        self.activeReservationsTestbedsDir = ""
        #self.activeReservationsReservationsDir = os.path.join( self.activeReservationsDir, 'reservations' )
        self.activeReservationsReservationsDir = ""
        #self.typeMapFile = os.path.join( self.reservationDir, 'typemap.yaml' )
        self.typeMapFile = ""
        self.pools = {}
        self.types = {}
        self.tempTestbed = []
        self.failedHostTypes = {}
        self.typeMap = {}
        
        #self.makeDirs()
    
    def initialize ( self, cfg ):
        self.cfg = cfg
        self.harnessCfg = cfg.harnessCfg
        self.reservationDir = self.harnessCfg.yaml['ITS_RESERVATION_DIR']
        self.poolsDir = os.path.join( self.reservationDir, 'pools' )
        self.typesDir = os.path.join( self.reservationDir, 'types' )
        self.activeReservationsDir = os.path.join( self.reservationDir, 'reservations' )
        self.activeReservationsHostsDir = os.path.join( self.activeReservationsDir, 'hosts' )
        self.activeReservationsTestbedsDir = os.path.join( self.activeReservationsDir, 'testbeds' )
        self.activeReservationsReservationsDir = os.path.join( self.activeReservationsDir, 'reservations' )
        self.typeMapFile = os.path.join( self.reservationDir, 'typemap.yaml' )
        self.makeDirs()
        
    def makeDirs ( self ):
        if not os.path.isdir( self.activeReservationsDir ):
            os.mkdir( self.activeReservationsDir )
        if not os.path.isdir( self.activeReservationsHostsDir ):
            os.mkdir( self.activeReservationsHostsDir )
        if not os.path.isdir( self.activeReservationsTestbedsDir ):
            os.mkdir( self.activeReservationsTestbedsDir )
        if not os.path.isdir( self.activeReservationsReservationsDir ):
            os.mkdir( self.activeReservationsReservationsDir )
    
    def populate ( self ):
        if self.args.action == 'reserve' and len( self.args.type ) == 0:
            self.populateTypeMap()
        self.populatePools()
        self.populateTypes()
        
    def populateTypeMap( self ):
        self.typeMap = yaml.load( open( self.typeMapFile, 'r' ) )
        #suite = os.path.split( self.args.suite )[-1]
        #suite = os.path.split( self.args.suitecfgfile )[-1]
        
        path, ext = os.path.splitext( self.args.suitecfgfile )
        key = self.args.suitecfgfile
        if len( self.cfg.testFile ):
            key = self.cfg.testFile
        
        self.args.type = self.typeMap[key]['type']
        self.args.pool = self.typeMap[key]['pool']
        
    def populatePools ( self ):
        for fileName in os.listdir( self.poolsDir ):
            path = os.path.join( self.poolsDir, fileName )
            poolName = os.path.splitext( fileName )[0]
            poolYAML = yaml.load( open( path, 'r' ) )
            self.pools[poolName] = poolYAML
            
    def populateTypes ( self ):
        for fileName in os.listdir( self.typesDir ):
            path = os.path.join( self.typesDir, fileName )            
            typeName = os.path.splitext( fileName )[0]
            poolYAML = yaml.load( open( path, 'r' ) )            
            self.types[typeName] = poolYAML
            
    def toString ( self ):
        s = self.toPoolsString()
        s += self.toTypesString()
        return s
    
    def toTypesString( self ):
        s = "=" * 30 + "\n"
        s += 'TYPES' + "\n"
        for typeName in self.types.keys():
            s += typeName + "\n"
            s += yaml.dump( self.types[typeName], default_flow_style=False )
        s += "=" * 30 + "\n"            
        return s
        
    def toPoolsString ( self ):
        s = "=" * 30 + "\n"
        s += 'POOLS' + "\n"
        for poolName in self.pools.keys():
            s += poolName + "\n"
            s += yaml.dump( self.pools[poolName], default_flow_style=False )
        s += "=" * 30 + "\n"                        
        return s
        
    def getTestbed ( self, type, pool, reservation ):
        regex = re.compile( type )
        testbed = []
        for name in self.types:
            if regex.match( name ):
                if int( self.args.verbose ) >= 1:
                    print " Matched Testbed Type: " + name
                testbed = self.tryProvisionType( name, pool, reservation )

                ### Fully provisioned
                if testbed:
                    if int( self.args.verbose ) >= 1:
                        print " Successfully Provisioned Testbed Type: " + name
                    break
                else:
                    if int( self.args.verbose ) >= 1:
                        print " Failed Provisioning Testbed Type: " + name                

        return name, testbed
    
    def tryProvisionType( self, name, pool, reservation):
        required = copy.deepcopy( self.types[name] )
        seen = {}
        for requiredNode in required:
            
            if int( self.args.verbose ) >= 2:   
                print "  Required Node: " + requiredNode['type']
            node = self.getNode( requiredNode, pool, seen, reservation )
            if node:
                if int( self.args.verbose ) >= 2:
                    print "   Matched: " + node['server'] + " " + node['type']
                self.tempTestbed.append( node )
                seen[node['server']] = node
            else:
                if requiredNode['type'] in self.failedHostTypes:
                    self.failedHostTypes[requiredNode['type']] += 1
                else:
                    self.failedHostTypes[requiredNode['type']] = 1
                if int( self.args.verbose ) >= 2:
                    print "   No Match"
                self.removeHostsLocks( self.tempTestbed )
                self.tempTestbed = []
                break
        return self.tempTestbed
                
    def removeHostsLocks( self, testbed ):
        if not testbed:
            return
        if int( self.args.verbose ) >= 1:
            print " Removing locked testbed hosts"

        for host in testbed:
            hostLockFilePath = os.path.join( self.activeReservationsHostsDir, host['server'] + '.yaml' ) 
            if os.path.exists( hostLockFilePath ):
                if os.path.isfile( hostLockFilePath ):
                    if int( self.args.verbose ) >= 2:
                        print " " + hostLockFilePath
                    os.remove( hostLockFilePath )
            
    def getNode ( self, requiredNode, pool, seen, reservation ):
        regex = re.compile( requiredNode['type'] )
        for node in self.pools[pool]:
            hostname = node['server']
            if hostname in seen:
                continue
            if regex.match( node['type']  ):
                lockFilePath = os.path.join( self.activeReservationsHostsDir, hostname + '.yaml' )
                success = self.writeHostLockFile( lockFilePath, reservation )
                if success:
                    return node
    
    def isHostReserved( self, host ):
        hostLockFilePath = os.path.join( self.activeReservationsHostsDir, host.server + '.yaml' ) 
        if os.path.exists( hostLockFilePath ) and os.path.isfile( hostLockFilePath ):
            return True
        return False
    
    def isTestbedFree( self, testbed ):
        for host in testbed.servers:
            if self.isHostReserved( host ):
                return False    
        return True
    
    def writeHostLockFile( self, lockFilePath, reservation ):
        res = { 'id' : reservation.id }
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            file_handle = os.open( lockFilePath, flags )
        except OSError as e:
            return False
        else:
            with os.fdopen( file_handle, 'w' ) as fileObj:
                fileObj.write( yaml.dump( res, default_flow_style=False ) )
            return True
        
    def getReservationsList( self ):
        allFiles = {}
        directory = self.activeReservationsReservationsDir
        files = os.listdir( directory )
        for resFile in files:
            reserveId, suffix = resFile.split( '.' )
            path = os.path.join( directory, resFile )
            allFiles[reserveId] = path
        return allFiles
        
    def toReservationsString( self ):
        allFiles = self.getReservationsList()
        s = ''
        if allFiles.keys():
            s += "=" * 30 + "\n"
        for reserveId in allFiles.keys():
            reservation = ItsReservation.ItsReservation( 
                id = reserveId,
                db = self,
            )
            reservation.thaw( reserveId, self.activeReservationsReservationsDir )
            s += reservation.toString()
        if allFiles.keys():
            s += "=" * 30
        return s
        