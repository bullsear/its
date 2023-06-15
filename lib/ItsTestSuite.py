"""ItsTestSuite.py - The List of Tests
NAME:
    ItsTestSuite.py - The List of Tests
"""

import os, sys, time, shutil, ItsException

class ItsTestSuite ( object ):

    def __init__( self ):
        self.tests = []
        self.passed = 0
        self.failed = 0
        self.unknown = 0
        self.rc = ""

    def toResultsMap( self ):
        testMap = {}
        for test in self.tests:
            testMap[test.testInstanceId] = test.result
        return testMap

    def toString ( self ):
        s = ""
        for test in self.tests:
            s += test.toString()
            s += "=" * 50 + "\n"
        return s
    
    def getTestsById( self, id ):
        tests = []
        for test in self.tests:
            if str( id ) == str( test.id ):
                tests.append( test )
        return tests

    def getAllWaitTests( self, waitTests ):
        tests = []
        for id in waitTests:
            found = self.getTestsById( id )
            for test in found:
                tests.append( test )
        return tests

    def computeResults( self ):

        for test in self.tests:
            if test.result == 'PASS':
                self.passed += 1
            elif test.result == 'FAIL':
                self.failed += 1
            else:
                self.unknown += 1
                
        if self.passed > 0 and self.failed == 0 and self.unknown == 0:
            self.rc = 0
            self.result = 'PASS'
            return 0
        else:
            self.rc = 1
            self.result = 'FAIL'
            return 1

    def getResults( self ):
        self.computeResults()
        return {
            'PASS' : str( self.passed ),
            'FAIL' : str( self.failed ),
            'UNKNOWN' : str( self.unknown ),
        }

    def getRunningTests( self ):
        running = []
        for test in self.tests:
            if test.isRunning():
                running.append( test )
        return running

    def getPreviousTests ( self, waiter ):
        previous = []
        for test in self.tests:
            if waiter.testInstanceId == test.testInstanceId:
                break
            previous.append( test )
        return previous
        
    def getAllWaitTests ( self, waitTestIds ):
        waitTests = []
        for testId in waitTestIds:
            #print testId
            waitTests.extend( self.getTestsById( testId ) )
        return waitTests
    
    def getAllBackgroundTests ( self ):
        background = []
        for test in self.tests:
            if test.background == "1":
                #print test.testInstanceId, test.background
                background.append( test )
        return background
        
    
    
    
    