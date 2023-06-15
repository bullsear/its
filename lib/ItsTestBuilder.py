"""ItsTestBuilder.py - Expand the Test Specs
NAME:
    ItsTestBuilder.py - Expand the Test Specs
"""

import os, sys, time, shutil, itertools
import ItsTestSuite, ItsTest, ItsException

class ItsTestBuilder ( object ):
    
    def __init__( self, runner ):
        self.runner = runner
        self.suiteCfg = runner.cfg.suiteCfg
        self.testbed = runner.testbed
        self.cfg = runner.cfg
        self.testSuite = ItsTestSuite.ItsTestSuite()
        self.ordinal = 0
        
    def expandTests ( self ):
                
        for testSpec in self.suiteCfg.yaml:

            loops = self.calculateLoops( testSpec );            
            #print loops
        
            servers = []
            if 'server' in testSpec:
                servers = self.testbed.getServers( { 'server' : testSpec['server'] } )
            elif 'type' in testSpec:
                servers = self.testbed.getServers( { 'type' : testSpec['type'] } )
            
            count = 1
            if 'count' in testSpec:
                count = testSpec['count']

            if servers:
                serverId = 1
                #instanceId = 1
                for server in servers:
                    self.expandCount( count, testSpec, server, serverId, loops )
                    serverId += 1
                #    instanceId += 1
            else:
                #instanceId = 1
                server = ""
                serverId = ""
                self.expandCount( count, testSpec, server, serverId, loops )

    def calculateLoops( self, testSpec ):
        iterations = ''
        loops = []
        if 'loop' in testSpec:
            for iterator in itertools.product( *testSpec['loop'] ):
                j = 0
                pairs = {}
                for i in iterator:
                    pairs[str(j)] = i
                    j += 1
                loops.append( pairs )
        return loops

    def expandCount ( self, count, testSpec, server, serverId, loops ):
        instanceId = 1       
        for i in range( count ):
            if loops:
                for loop in loops:
                    self.buildTest( testSpec, server, serverId, instanceId, self.runner.runDir, self.runner.cfg.baseDir, self.cfg, loop )
            else:
                self.buildTest( testSpec, server, serverId, instanceId, self.runner.runDir, self.runner.cfg.baseDir, self.cfg, "" )
            instanceId += 1

    def buildTest( self, testSpec, server, serverId, instanceId, runDir, baseDir, cfg, loop ):
        self.ordinal += 1
        test = ItsTest.ItsTest( testSpec, self.ordinal, server, serverId, instanceId, runDir, baseDir, cfg, loop, self.runner )
        self.testSuite.tests.append( test )
        instanceId += 1
    

                