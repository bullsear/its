"""ItsTime.py - Time Utilities
NAME:
    ItsTime.py - Time Utilities
"""

import os, sys, time, yaml, datetime, shutil
import ItsException

class ItsTime ( object ):
    
    def __init__( self ):
        pass
    
    def dateTimeStamp ( self ):
        dateTime = datetime.datetime.now()
        milliSeconds = str( dateTime.microsecond ).ljust( 6, '0' )
        epoch = str( int( time.mktime( dateTime.timetuple() ) ) )
        t = datetime.datetime.fromtimestamp( float( epoch ) )
        fmt = "%Y-%m-%d %H:%M:%S"
        return t.strftime( fmt ) + '.' + milliSeconds

    def getHighResolutionEpoch ( self ): 
        dateTime = datetime.datetime.now()
        epoch = str( int( time.mktime( dateTime.timetuple() ) ) ) + '.' + str( dateTime.microsecond ).ljust( 6, '0' )
        return epoch
    

    
    