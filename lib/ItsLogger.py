"""ItsLogger.py - Log Utilities
NAME:
    ItsLogger.py - Log Utilities
"""

import os, sys, time, yaml, datetime, shutil, socket
import ItsException, ItsTime

class ItsLogger ( object ):
    
    def __init__( self, runner, cfg ):
        self.runner = runner
        self.cfg = cfg
        self.harnessLog = ""
        self.harnessLogHandle = ""
        self.runner.logger = self
        self.resultsLog = ""
        self.resultsMapLog = ""
        self.runMetaLog = ""
        self.time = ItsTime.ItsTime()
        self.pidLog = ''

    def prepLogs ( self ):
        self.prepRunDir()
        self.copyConfigs()
        self.pidLog = os.path.join( self.runner.runDir, 'pid.log' )
        self.createPidFile()
        self.harnessLog = os.path.join( self.runner.runDir, 'harness.log' )
        self.resultsLog = os.path.join( self.runner.runDir, 'results.yaml' )
        self.resultsMapLog = os.path.join( self.runner.runDir, 'results_map.yaml' )
        self.runMetaLog = os.path.join( self.runner.runDir, 'run.yaml' )
        self.harnessLogHandle = open( self.harnessLog, 'a' )
        
    def createPidFile ( self ):
        handle = open( self.pidLog, 'w' )
        handle.write( str(os.getpid()) )
        handle.close()
        
    def copyConfigs ( self ):
        
        shutil.copyfile( self.cfg.harnessCfg.file, os.path.join( self.runner.cfgDir, 'harness.yaml' ) )
        if self.cfg.parameterCfg != "":
            shutil.copyfile( self.cfg.parameterCfg.file, os.path.join( self.runner.cfgDir, 'parameter.yaml' ) )
        shutil.copyfile( self.cfg.suiteCfg.file, os.path.join( self.runner.cfgDir, 'suite.yaml' ) )
        shutil.copyfile( self.cfg.testbedCfg.file, os.path.join( self.runner.cfgDir, 'testbed.yaml' ) )
        
        handle = open( os.path.join( self.runner.cfgDir, 'environment.txt' ), 'a' )
        handle.write( self.cfg.dumpEnv() )
        handle.close
        
    def prepRunDir ( self ):
        
        logDir = "/tmp/ist/log"
        if 'ITS_LOGDIR' in self.cfg.harnessCfg.yaml:
            logDir = self.cfg.harnessCfg.yaml['ITS_LOGDIR']
        
        id = ""
        runDir = ""
        
        for i in range( 1, 1001 ):

            id = self.runner.generateRunId()
            runDir = os.path.join( logDir, id )
            
            try: 
                os.makedirs( runDir )
                self.runner.runId = id
                self.runner.runDir = runDir
                #self.runner.runURL = self.cfg.harnessCfg.yaml['ITS_ROOT_URL'] + self.runner.runId
                self.runner.runURL = ''.join( [ 'http://', socket.getfqdn(), '/itslogs/', self.runner.runId ] )
                break
            except Exception as e:
                pass
            
        
        self.runner.cfgDir = os.path.join( runDir, "cfg" )
        
        os.environ['ITS_RUNID'] = self.runner.runId
        os.makedirs( self.runner.cfgDir )
        
    def write( self, tag, line ):
        timestamp = self.time.dateTimeStamp()
        line = ' '.join( [ timestamp, ":", tag, line ] )
        #self.harnessLogHandle.write( line + "\n" )
        #print line
        self.writeBoth( line )
        return timestamp
    
    def writeBoth( self, input ):
        #if self.harnessLogHandle.closed:
        #    self.harnessLogHandle = open( self.harnessLog, 'a' )
        self.harnessLogHandle.write( input + "\n" )
        print input
        
    def line1 ( self ):
        s = "=" * 65
        return s        
        
    def writeMetaBoth ( self ):
        self.writeBoth( self.toMetaString() )
        
    def toMetaString ( self ):
        s = self.line1() + "\n\n"
        s += "                    Integrated Test System\n\n" 
        s += "Harness PID:           " + self.runner.pid + "\n"
        s += "Run Log Directory:     " + self.runner.runDir + "\n"
        s += "Run Log URL:           " + self.runner.runURL + "\n\n"
        if self.cfg.parameterCfg != "":
            s += "Parameter Config File: " + self.cfg.parameterCfg.file + "\n"
        s += "Testbed Config File:   " + self.cfg.testbedCfg.file + "\n"
        s += "Suite Config File:     " + self.cfg.suiteCfg.file + "\n"
        s += "\n" + self.line1() + "\n"
        return s

    def showResults ( self, results, resultsMap ):
        
        summary = self.resultsSummary( results )
                
        self.writeResultsLog( results )
        self.writeResultsMapLog( resultsMap )
        self.writeBoth( summary )
        
    def resultsSummary ( self, results ):
        s = "                             RESULTS\n"
        s += "PASS:    " + results['PASS'] + "\n"
        s += "FAIL:    " + results['FAIL'] + "\n"
        s += "UNKNOWN: " + results['UNKNOWN'] + "\n\n"
        for test in self.runner.testSuite.tests:
            if not len(test.testInstanceId ):
                test.setTestInstanceId()
            result = "UNKNOWN"
            if len(test.result):
                result = test.result
            pad = ' ' * ( 45 - len( test.testInstanceId ) )
            s += test.testInstanceId + ':' + pad + result + "\n"
        s += "\n" + self.line1() + "\n"
        return s
        
    def writeResultsLog( self, results ):
        yaml.dump( results, file( self.resultsLog, 'w' ), default_flow_style=False )

    def writeResultsMapLog( self, resultsMap ):
        yaml.dump( resultsMap, file( self.resultsMapLog, 'w' ), default_flow_style=False )
        
    def writeRunMeta( self, run ):
        #yaml.dump( run.__dict__, file( self.runMetaLog, 'w' ), default_flow_style=False )
        run.freeze( self.runMetaLog )
    
    
    
    
    
    
    
    
    
    
    