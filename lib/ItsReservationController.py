"""ItsReservationController.py - Reservations Command Controller
NAME:
    ItsReservationController.py - Reservations Command Controller
"""

import os, sys, time, collections
import ItsException, ItsReservationLogger, ItsReservationDatabase, ItsReservationDispatcher, ItsReserveSignals

class ItsReservationController ( object ):
    
    def __init__( self, cfg, args ):
        self.cfg = cfg
        self.args = args
    
    def do( self ):
    
        # Start the rotating logging
        logger = ItsReservationLogger.ItsReservationLogger( self.cfg.harnessCfg )
        
        # Intialize the database
        #db = ItsReservationDatabase.ItsReservationDatabase( self.cfg, self.args, logger )
        db = ItsReservationDatabase.ItsReservationDatabase()
        db.initialize( self.cfg )
        db.args = self.args
        db.logger = logger
        db.populate()
        
        # Dispatch the command and execute
        dispatcher = ItsReservationDispatcher.ItsReservationDispatcher( self.args, db )
        sigs = ItsReserveSignals.ItsReserveSignals( dispatcher ).register()
        path = dispatcher.do()
        
        if path and len( path ):
            #print path
            return path
        else:
            return ""
    
    #def unreserveTestbed( self ):
    #        
    #    # Start the rotating logging
    #    logger = ItsReservationLogger.ItsReservationLogger( self.cfg.harnessCfg )
    #    
    #    # Intialize the database
    #    db = ItsReservationDatabase.ItsReservationDatabase( self.cfg.harnessCfg, self.args, logger )
    #    db.populate()
    #    
    #    # Dispatch the command and execute
    #    dispatcher = ItsReservationDispatcher.ItsReservationDispatcher( self.args, db )
    #    sigs = ItsReserveSignals.ItsReserveSignals( dispatcher ).register()
    #    path = dispatcher.do()
    

