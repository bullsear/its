"""ItsAssert.py - Assertions
NAME:
    ItsAssert.py - Assertions
"""

import os, sys, re
import ItsException, ItsTime
from numbers import Number

class ItsAssertion ( object ):
    
    def __init__ ( self ):
        self.time = ItsTime.ItsTime()
        self.results = { 'pass' : 0, 'fail' : 0 }
        self.all = []
        self.verification = 0

    def verify ( self, conditional, comment ):
            
        #print type( conditional )
        
        # None
        if conditional is None:
            #print "None branch"
            self.not_ok( conditional, comment )
        
        # boolean: True means PASS
        elif isinstance( conditional, (bool) ):
            #print "bool branch"
            if conditional:
                self.ok( conditional, comment )
            else:
                self.not_ok( conditional, comment )        
        
        # string
        elif isinstance( conditional, basestring ):
            #print "String branch"
            if len( conditional ) > 0:
        
                result = False
                try:
                    result = eval( str( conditional ) )
                except Exception as e:
                    raise ItsException.ItsAssertionException( "Un-eval-able string." )
                
                if result:
                    self.ok( conditional, comment )
                else:
                    self.not_ok( conditional, comment )
                    
            else:
                self.not_ok( conditional, comment )        
        
        elif isinstance( conditional, Number ):
            #print "Number branch"
            if eval( str( conditional ) ):
                self.not_ok( conditional, comment )
            else:
                self.ok( conditional, comment )

        # Any 'object' passes (intended for successful re.search())
        elif isinstance( conditional, object ):
            #print "Object branch"
            self.ok( conditional, comment )            
        
        # # string
        # elif isinstance( conditional, basestring ):
        #     print "String branch"
        #     if len( conditional ) > 0:
        # 
        #         result = False
        #         try:
        #             result = eval( str( conditional ) )
        #         except Exception as e:
        #             raise ItsException.ItsAssertionException( "Un-eval-able string." )
        #         
        #         if result:
        #             self.ok( conditional, comment )
        #         else:
        #             self.not_ok( conditional, comment )
        #             
        #     else:
        #         
        #         self.not_ok( conditional, comment )
                
        # # boolean: True means PASS
        # elif isinstance( conditional, (bool) ):
        #     print "bool branch"
        #     if conditional:
        #         self.ok( conditional, comment )
        #     else:
        #         self.not_ok( conditional, comment )
                
        # number; ZERO MEANS PASS!!!  
        # else:
        #     print "int branch"
        #     if eval( str( conditional ) ):
        #         self.not_ok( conditional, comment )
        #     else:
        #         self.ok( conditional, comment )
    
    def result ( self, tag, comment ):
        self.verification += 1
        if tag == 'PASS':
            self.results['pass'] += 1
        elif tag == 'FAIL':
            self.results['fail'] += 1
        else:
            pass
        string = [
            self.time.dateTimeStamp(),
            "RESULT  ",
            "\"" + str( comment ) + "\"",
            str( tag ),
        ]
        string = " ".join( string )    
        self.all.append( string )    
        print string
    
    def ok ( self, conditional, comment ):
        self.results['pass'] += 1
        print self.show( "PASS", conditional, comment )
    
    def not_ok ( self, conditional, comment ):
        self.results['fail'] += 1
        print self.show( "FAIL", conditional, comment )
        
    def show ( self, tag, conditional, comment ):
        self.verification += 1
        string = [
            self.time.dateTimeStamp(),
            "VERIFY  ",
            "(" + str( conditional ) + ")",
            "\"" + str( comment ) + "\"",
            str( tag ),
        ]
        string = " ".join( string )
        self.all.append( string )
        return string
    
    #atexit.register( end )

    
    