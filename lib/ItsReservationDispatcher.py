"""ItsReservationDispatcher.py - Reservations Command Dispatcher
NAME:
    ItsReservationDispatcher.py - Reservations Command Dispatcher
"""

import os, sys, time, collections
import ItsException, ItsReservation, ItsTime

class ItsReservationDispatcher ( object ):
    
    def __init__( self, args, db ):
        self.args = args
        self.db = db
        self.logger = db.logger
        self.reservation = ""
        
    def do ( self ):
        if self.args.action == 'showtypes':
            print self.db.toTypesString(),
        elif self.args.action == 'showpools':
            print self.db.toPoolsString(),
        elif self.args.action == 'showall':
            print self.db.toTypesString(), self.db.toPoolsString(),
        elif self.args.action == 'showreservation':
            self.showReservation( self.args.reserveId )
        elif self.args.action == 'showallreservations':
            self.showAllReservations()
        elif self.args.action == 'reserve':
            return self.reserve()
        elif self.args.action == 'unreserve':
            self.unreserve( self.args.reserveId )
        elif self.args.action == 'update':
            self.update( self.args.reserveId, self.args.duration )
    
    def reserve ( self ):

        self.reservation = ItsReservation.ItsReservation(
            type = self.args.type, 
            pool = self.args.pool, 
            user = self.args.user, 
            duration = self.args.duration,
            db = self.db,
        )
        
        logParams = [ self.args.type, self.args.pool, self.args.user, self.args.duration, self.reservation.id ]
        self.logger.write( 'REQUEST', " ".join( logParams ) )

        provisionedType, provisionedTestbed = self.getTestbed( self.args.type, self.args.pool, self.reservation )
        
        # Successfully provisioned!
        if provisionedTestbed:   
            self.setReservation( provisionedType, provisionedTestbed )
            logParams = [ self.reservation.type, self.reservation.pool, self.reservation.user, self.reservation.duration, self.reservation.id ]
            self.logger.write( 'RESERVE', " ".join( logParams ) )
            output = self.reservation.file
            if self.args.verbose >= 1:
                output += " (" + self.reservation.type + ")"
            return output
        # Provisioning failed.
        else:
            if self.args.verbose >= 1:
                print ItsTime.ItsTime().dateTimeStamp() + " : Provisioning ultimately failed"
            for i in self.db.failedHostTypes:
                self.logger.write( 'HOSTFAIL', " ".join( [ i, str( self.db.failedHostTypes[i] ) ] ) )
            logParams = [ self.args.type, self.args.pool, self.args.user, self.args.duration ]
            self.logger.write( 'TESTBEDFAIL', " ".join( logParams ) )
            #sys.exit( 1 )
            return ""
    
    def unreserve ( self, reserveId ):
        self.reservation = ItsReservation.ItsReservation( 
            id = reserveId,
            db = self.db,
        )
        self.reservation.endTime = ItsTime.ItsTime().dateTimeStamp()
        if self.args.verbose >= 1:
            print ItsTime.ItsTime().dateTimeStamp() + " : Unprovisioning reservation " + self.reservation.id
        logParams = [ self.reservation.id ]
        self.logger.write( 'UNRESERVE', " ".join( logParams ) )
        self.reservation.removeReservation()
        
    def update ( self, reserveId, duration ):
        self.reservation = ItsReservation.ItsReservation( 
            id = reserveId,
            db = self.db,
        )
        if self.args.verbose >= 1:
            print ItsTime.ItsTime().dateTimeStamp() + " : Unprovisioning reservation " + self.reservation.id   
        self.reservation.updateReservationDuration( self, duration )
        
    def getTestbed ( self, requiredType, pool, reservation ):
        for i in range( 0, int( self.args.iterations ) ):
            if self.args.verbose >= 1:
                print ItsTime.ItsTime().dateTimeStamp() + " : Provisioning attempt " + str( i + 1 )
            provisionedType, provisionedTestbed = self.db.getTestbed( requiredType, pool, reservation )
            if provisionedTestbed:
                return provisionedType, provisionedTestbed
            time.sleep( int( self.args.sleep ) )
        return "", []

    def setReservation ( self, provisionedType, provisionedTestbed ):
        self.reservation.type = provisionedType
        self.reservation.testbed = provisionedTestbed        
        self.reservation.create( self )
        
    def showReservation ( self, reserveId ):
        self.reservation = ItsReservation.ItsReservation( 
            id = reserveId,
            db = self.db,
        )
        self.reservation.thaw( reserveId, self.db.activeReservationsReservationsDir )
        print self.reservation.toString(),
        
    def showAllReservations( self ):
        print self.db.toReservationsString()
            

        