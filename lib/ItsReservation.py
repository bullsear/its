"""ItsReservation.py - Reservation Data Object
NAME:
    ItsReservation.py - Reservation Data Object
"""

import os, sys, yaml, uuid
import ItsException, ItsTime, ItsReservationDatabase

class ItsReservation ( object ):
        
    def __init__( self, type="", file="", pool="", user="", duration="", startTime="", endTime="", id="", db="" ):
        if len( id ):
            self.id = id
            self.db = db
            self.reservationFile = os.path.join( db.activeReservationsReservationsDir, self.id + '.yaml' )
            self.file = os.path.join( db.activeReservationsTestbedsDir, self.id + '.yaml' )
        else:
            self.id = uuid.uuid4().hex
            self.file               = file   
            self.reservationFile    = ""
            self.testbed            = ""
            self.db                 = ""
        self.type               = type
        self.pool               = pool   
        self.user               = user
        self.duration           = duration
        self.startTime          = startTime
        self.endTime            = endTime
        
    def removeReservation ( self ):
        if os.path.isfile( self.file ):
            self.testbed = yaml.load( open( self.file, 'r' ) )
            #print self.testbed
            self.delete()
            self.db.removeHostsLocks( self.testbed )
            ### This should probably search grep for individual hosts too
        else:
            pass
    
    def create ( self, dispatcher ):
        self.file = os.path.join( dispatcher.db.activeReservationsTestbedsDir, self.id + '.yaml' )
        self.reservationFile = os.path.join( dispatcher.db.activeReservationsReservationsDir, self.id + '.yaml' )
        self.startTime = ItsTime.ItsTime().dateTimeStamp()
        yaml.dump( self.__dict__, file( self.reservationFile, 'w' ), default_flow_style=False )
        yaml.dump( self.testbed, file( self.file, 'w' ), default_flow_style=False )
        os.chmod( self.reservationFile, 0777 )
        os.chmod( self.file, 0777 )
    
    def delete ( self ):
        if isinstance( self.db, ItsReservationDatabase.ItsReservationDatabase ) and int( self.db.args.verbose ) >= 2:
            print " Removing reservation files"
        if os.path.isfile( self.file ):
            if int( self.db.args.verbose ) >= 2:
                print " " + self.file
            os.remove( self.file )
        if os.path.isfile( self.reservationFile ):
            if int( self.db.args.verbose ) >= 2:
                print " " + self.reservationFile            
            os.remove( self.reservationFile )
            
    def updateReservationDuration ( self, dispatcher, duration ):
        self.thaw( self.id, dispatcher.db.activeReservationsReservationsDir )
        #print self.toString()
        self.duration = duration
        yaml.dump( self.__dict__, file( self.reservationFile, 'w' ), default_flow_style=False )
        
    def thaw ( self, reserveId, reservationsDir ):
        filePath = os.path.join( reservationsDir, reserveId + '.yaml' )
        #print filePath
        attributes = yaml.load( open( filePath, 'r' ) )
        #print attributes
        for key in attributes.keys():
            setattr( self, key, attributes[key] )
#        print self.toString()
    
    def toString ( self ):
        s = "************* RESERVATION *************\n";
        attributes = self.__dict__.copy()
        if 'db' in attributes:
            del attributes['db']
        s += yaml.dump( attributes, default_flow_style=False )
        return s
        
        
        
    