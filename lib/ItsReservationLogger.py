"""ItsReservationLogger.py - Log Utilities
NAME:
    ItsReservationLogger.py - Log Utilities
"""

import os, sys, glob, shutil
import ItsException, ItsTime

class ItsReservationLogger ( object ):
    
    def __init__( self, cfg, maxsize=10000000, count=10 ):
        self.cfg = cfg
        self.maxsize = maxsize
        self.count = count
        #self.logDir = os.path.self.cfg.yaml['ITS_RESERVATION_LOGDIR']
        self.logDir = os.path.join( self.cfg.yaml['ITS_RESERVATION_DIR'], 'logs' )
        if not os.path.exists( self.logDir ):
            os.makedirs( self.logDir )
        self.logFilePath = os.path.join( self.logDir, 'reserve.1.log' )
        self.time = ItsTime.ItsTime()

    def write ( self, tag, line ):
        self.checkRotate()
        timestamp = self.time.dateTimeStamp()
        line = ' '.join( [ timestamp, ":", tag, line ] )
        self.tryWrite( line )
        
    def tryWrite( self, line ):
        for i in range( 21 ):
            try:
                logFile = open( self.logFilePath, 'a' )
                logFile.write( line + "\n" )
                logFile.close()
                break
            except:
                continue
        
    def checkRotate( self ):
        if not os.path.exists( self.logFilePath ):
            return
        size = os.stat( self.logFilePath ).st_size
        if size > self.maxsize:
            self.rotate()
            
    def rotate ( self ):
        files = glob.glob( os.path.join( self.logDir, 'reserve.*.log*' ) )
        if files:
            sortedLogs = self.sortLogs( files )
            self.moveLogs( sortedLogs )
        
    def sortLogs( self, files ):
        logs = {}
        for logName in files:
            path, i, suffix = logName.split( '.' )
            logs[int(i)] = logName
        sortedLogs = []
        for i in sorted( logs.keys(), key=int ):
            sortedLogs.insert( 0, logs[i] )
        return sortedLogs
            
    def moveLogs( self, sortedLogs ):
        for log in sortedLogs:
            path, i, suffix = log.split( '.' )
            newInt = int(i) + 1
            newLog = '.'.join( [ path, str(newInt), suffix ] )
            if (int(i) + 1) > self.count:
                os.remove( log )
            else:
                shutil.move( log, newLog )
        
            