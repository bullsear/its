"""ItsReserveSignals.py - Signal Handling
NAME:
    ItsReserveSignals.py - Signal Handling
"""

import os, sys, socket, time, signal
import ItsReservation, ItsTime

class ItsReserveSignals ( object ):

    def __init__( self, dispatcher ):
        self.dispatcher = dispatcher
    
    def register ( self ):
        signal.signal( signal.SIGINT, self.handle_cntl_c )    

    def handle_cntl_c( self, signal, frame ):
        print
        if self.dispatcher.args.verbose >= 1:
            print "HANDLING CNTL-C"
        if not isinstance( self.dispatcher.reservation, basestring ) and isinstance( self.dispatcher.reservation, ItsReservation.ItsReservation ):
            if self.dispatcher.args.verbose >= 1:
                print ItsTime.ItsTime().dateTimeStamp() + " : Rolling back reservation"
            self.dispatcher.reservation.delete()
        self.dispatcher.db.removeHostsLocks( self.dispatcher.db.tempTestbed )
        sys.exit( 1 )




