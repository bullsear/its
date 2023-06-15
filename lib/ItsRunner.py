"""ItsRunner.py - Its Suite Runner
NAME:
    ItsRunner.py - Its Suite Runner
"""

import os, sys, socket, time, subprocess, threading, signal, pprint
import ItsTestBuilder, ItsException, ItsSignals, ItsMail, ItsTime, ItsRun, ItsCLIParser

class ItsRunner ( object ):
    
    def __init__( self, cfg, testbed ):
        self.cfg = cfg
        self.testbed = testbed
        self.runId = ""
        self.runDir = ""
        self.cfgDir = ""
        self.pid = self.cfg.pid
        self.testSuite = ""
        self.logger = ""
        self.killAll = 0
        self.signals = ItsSignals.ItsSignals( self )
        self.startTime = ""
        self.endTime = ""
        self.hostname = socket.getfqdn()
        self.runURL = ""
        self.endedBatch = False
        self.prettyPrinter = pprint.PrettyPrinter( indent=4 )                                
        self.parser = ItsCLIParser.ItsCLIParser()        

    def generateRunId ( self ):
        id = str( int( time.time() ) ) + '.' + socket.gethostname()
        return id
    
    def buildTestList ( self ):
        builder = ItsTestBuilder.ItsTestBuilder( self )
        builder.expandTests()
        self.testSuite = builder.testSuite
        
    def run ( self ):
        
        self.logger.writeMetaBoth()
        if not self.cfg.arguments.nocheck:
            self.checkTestbedSsh()
        self.logger.write( "START BATCH", "" )
        self.startBatch()
        
        # Start all test processes here
        for test in self.testSuite.tests:
            
            if self.killAll == 1:
                break
            
            # Block on these
            self.startTest( test )
        
        if self.testSuite.getAllBackgroundTests():
            if self.cfg.arguments.verbose > 0:
                self.logger.write( "WAITING ON REMAINING BACKGROUND PROCESSES", "" )
            
        self.endBackgroundedTests()
            
        self.endBatch()
        
    def checkTestbedSsh ( self ):
        self.logger.write( "START CHECK TESTBED", "" )
        self.testbed.checkAllServersSsh()
        self.logger.write( "END CHECK TESTBED", "" )
        self.logger.writeBoth( "\n" + self.logger.line1() + "\n" )        
        
    def setEnv ( self ):
        os.environ['ITS_TESTBED'] = self.cfg.testbedCfg.file
        os.environ['ITS_RUNID'] = self.runId
    
    def startTest ( self, test ):
        
        time.sleep( float( test.presleep ) )   
        
        if test.wait != "" and test.wait != None:
            ###self.wait_all( test.wait, test )
            self.waitOnTests( self.testSuite.getAllWaitTests( test.wait ) )
        
        test.initialize( self.runDir, self.logger )

        test.proc = subprocess.Popen(
            test.getCommand(),
            shell = True,
            preexec_fn = os.setsid,
            ### Doesn't work
            env=os.environ.copy(),
        )
        
        test.pid = test.proc.pid
        
        # Start the timer
        if test.timeout != "":
            test.timer = threading.Timer( float( test.timeout ), self.timeOut, [test] )
            test.timer.start()
        
        test.writeMeta()
        
        # Blocking, non-backgrounded tests end here
        if test.background != "1":
            test.proc.wait()
            test.rc = test.proc.returncode      
            #test.getTestReturnCode()    ###

            self.testResult( test )
            
            #test.markEnd( self.logger )###
            
        test.postSleep()
        
    def waitOnTests ( self, testsToWaitOn ):
        for test in testsToWaitOn:
            if self.cfg.arguments.verbose > 0:
                self.logger.write( "WAITING ON", test.testInstanceId )
            test.proc.wait()
            test.rc = test.proc.returncode
            self.testResult( test )
           
    def timeOut( self, test ):
        if test.proc is not None and test.proc.poll() is None:
            self.logger.write( "TIMEOUT", test.testInstanceId )
            test.proc.kill()
            test.rc = test.proc.returncode      
            test.timer.cancel()
        
    def endBackgroundedTests( self ):
        
        #for test in self.testSuite.tests:
        for test in self.testSuite.getAllBackgroundTests():
            #print test.instanceId
            test.proc.wait()
            #test.getTestReturnCode()    ###
            test.rc = test.proc.returncode      # -9 means timeout?        ### This isn't the remote code!!!
            self.testResult( test )
            #test.markEnd( self.logger )            
    
#    def endBackgroundedTests( self ):
#            
#        for test in self.testSuite.tests:
#            if test.result == "" and test.proc != "":
##            print test.testInstanceId, test.background
##            if test.background == 1 and test.result == "":
##                if test.proc.poll() != None:
#                    ###
##                    test.proc.wait()
#                    test.rc = test.proc.returncode
#                    self.testResult( test )
#            test.postSleep()
    
    def registerSignalHandlers ( self ):
        self.signals.register()
        
    def wait_all( self, waitTestIds, waiter ):
     
        tests = []
        # Wait on all the previous tests to exit
        if waitTestIds == 'previous':
            tests = self.testSuite.getPreviousTests( waiter )
        # Wait on specified tests to exit
        else:
            tests = self.testSuite.getAllWaitTests( waitTestIds )

        if tests:
            self.waitThese( tests, waitTestIds, waiter )
        
    def waitThese( self, tests, waitTestIds, waiter ):
          
        #message = 'WAITING ON PREVIOUS PROCESSES'
        #if waitTestIds != 'previous':
            #ids = []
            #for id in waitTestIds:
            #    ids.append( str( id ) )
            #message = 'WAITING ON PROCESSES: ' + ",".join( ids )
            #self.logger.write( message, '' )
        
        for test in tests:
            #print " " + waiter.instanceId + " => " + test.testInstanceId
            #test.proc.wait()
            self.waitTest( test )
    
    def waitTest ( self, test ):
        #self.logger.write( " WAITING ON TEST", test.testInstanceId )
        while True:
            if not test.isRunning():
                #test.markEnd( self.logger )
                #self.logger.write( " ENDING TEST", test.testInstanceId + str(test.proc.returncode) )    ###
                #print test.proc.returncode
                #test.rc = str(test.proc.returncode)
                #test.proc.wait()
                #test.rc = test.proc.returncode          
                self.testResult( test )
                return
    
    def allDone( self ):
        for test in self.testSuite.tests:
            #if test.result == "":
            #if test.proc != "" and test.proc.poll() is not None:
            #    return False
            if test.isRunning():
                return False
        return True        

    def testResult( self, test ):
        
        ### This appears to have no effect
        #if test.rc == '' and test.proc != "" and test.proc.poll() is not None:
            #for i in range( 1, 10 ):
                #time.sleep( 1 )
            #test.getTestReturnCode()
            #print test.pid
            #print test.proc
            #print test.proc.wait()
            #test.proc.wait()
        ### This works only during "WAITING ON ALL BACKGROUND PROCESSES"
        ### Other processes show 'None' rc
        #test.rc = test.proc.returncode
        #print test.rc
        #print test.proc.wait()
        
        if int( test.ignore ) == 1:
            test.result = 'PASS'
        else:
            if test.rc == "":
                test.result = 'UNKNOWN'
            elif test.rc == 0:
                test.result = 'PASS'
            elif test.rc != 0:
                test.result = 'FAIL'
            
        test.markEnd( self.logger )
        #test.writeMeta()

        if test.haltonfail == "1" and test.result == 'FAIL' and not self.killAll == "1":
            self.logger.write( "HALTING ON TEST FAILURE", test.testInstanceId )
            tests = self.testSuite.tests
            self.killAllTests( tests )

    def killAllTests( self, tests ):
        self.killAll = 1
        for test in tests:
            if test.proc is not None and test.proc is not '' and test.proc.poll() is None:
                self.logger.write( "KILLING TESTER PROCESS", test.testInstanceId )
                #test.proc.kill()
                ### test.proc.kill() doesn't kill the sshpass process launched by ssh.bash
                os.killpg( test.proc.pid, signal.SIGTERM )
                self.testResult( test )
        self.killRemoteProcesses()
        self.endBatch()
        
    def killRemoteProcesses ( self ):
        clientProcesses = {}
        ### TODO: try all the nodes
        for client in self.testbed.getServers( { 'type' : 'linux_client' } ):
            self.logger.write( "KILLING CLIENT PROCESSES ON ", client.server )
            # Get remote parent PID(s)
            out, rc = client.send( 'ps -ef | grep ' + self.pid ).complete()
            parents = self.parser.grepTable( out, matchString='ITS_HOST_PID=' + self.pid )            
            ppids = []
            kids = []
            # Find the kids
            for proc in parents:
                ppid = proc.split()[1]
                ppids.append(ppid)
                out, rc = client.send( 'ps --ppid ' + ppid ).complete()
                lines = out.splitlines()
                if len(lines):
                    lines.pop(0)
                for line in lines:
                    pid = line.split()[0]
                    kids.append( pid )
            # Kill the kids, the parents
            for pid in kids:
                out, rc = client.send( 'kill -9 ' + pid ).complete()

    def startBatch( self ):
        self.startTime = self.logger.time.dateTimeStamp()
        self.setEnv()
        self.logger.writeRunMeta( self.getRunMeta() )
        self.sendMail( self.logger.toMetaString(), 'ITS Start Job ' + self.runId )
        
    def endBatch( self ):
        if self.endedBatch:
            return
        self.endTime = self.logger.time.dateTimeStamp()
        self.logger.writeRunMeta( self.getRunMeta() )        
        self.logger.write( "END BATCH", "\n" )        
        self.logger.writeMetaBoth()
        self.logger.showResults( self.testSuite.getResults(), self.testSuite.toResultsMap() )
        self.sendMail( self.logger.toMetaString() + "\n" + self.logger.resultsSummary( self.testSuite.getResults() ), 'ITS End Job ' + self.runId )          
        self.logger.harnessLogHandle.close()
        self.cfg.cleanup()
        self.endedBatch = True
        
    def getRunMeta( self ):
        return ItsRun.ItsRun( self )

    def sendMail( self, text, title ):
        
        if len(self.cfg.arguments.subject):
            title += ' ' + self.cfg.arguments.subject
            
        success = True
        for i in range( 10 ):
            try:
                mail = ItsMail.ItsMail()
                mail.mailTo = self.cfg.arguments.email
                mail.subject = title
                mail.text = text
                mail.send()
                success = True
                break
            except Exception as e:
                #print e
                success = False
                time.sleep( 60 )
                continue
        
        if not success:
            #print "ERROR: Email failed"
            self.logger.write( "ERROR: Email failed" ) 
        
    def toString ( self ):
        s = ""
        s += "* ItsRunner\n"
        return s

