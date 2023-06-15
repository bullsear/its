#!/usr/bin/env python

"""its.py - Integrated Test System
NAME:

    its.py - Multi-Threaded Distributed System Test Harness and Reservation System

SYNOPSIS:

    # Reserve a testbed of the specified type from a provisioning pool for 30 minutes
    $> its -a reserve -y <type> -c <pool> -u <username> -n 30
    
    # Run a test suite with a previously provisioned testbed 
    $> its -a run -t <testbed> -s <suite> -u <username>
    
    # Auto-provisioning the appropriate testbed, run a suite, and un-provision the testbed
    $> its -a run -s <suite> -u username>

ARGUMENTS:

    -a = Action (run|reserve|unreserve|update|showreservation|showallreservations|showtypes|showpools|showall) 
    -u = Username
    
    -t = Path to testbed descriptor configuration file 
    -s = Path to test specification configuration file 
    -p = Path to test run parameter configuration file
    -x = Don't check testbed ssh connectivity before executing tests
    
    -y = Testbed type
    -c = Provisioning pool
    -n = Reservation duration, in minutes
    -i = Reservation attempt retry count
    -e = How long to sleep between reservation attempts 
    
    -h = Display this documentation
    -v = Verbosity level

    * Note: The configuration files must be in valid YAML format 

DESCRIPTION:

    This is a multi-threaded system test harness designed for testing distributed software
    systems.  The harness is designed to be run on a Linux host.  All the processes are
    referred to as 'tests'.
    
    Tests can be on the local host or executed remotely via ssh.  They can block until
    completion or be backgrounded.  Tests can wait on previously backgrounded tests to exit.
    Multiple identical processes can be launched by a single specification.  The harness
    can sleep after a process.  The user can provide environment variables that can be
    accessed by subprocesses.

    The harness will report when processes are started and end and summarize test exit
    status at the end of a run.
    
RUN LOGS:

    The master harness process creates a unique run log directory.  The directory name is
    guaranteed to be unique even if the directory is shared by multiple users from multiple 
    hosts.  Configurations files are copied to the run directory at the beginning of every
    run to enable repeatability.
 
    Here is an example of the logs created:
    
    1427225937.todd1/                       # Run directory (epochseconds.hostname)
    
        000001_localhost_hostname_123/      # Sub-process directory for each sub-process
    
            environment.txt                 # Sub-process environment variable list
            meta.log                        # Sub-process metadata process attributes
            output.log                      # Sub-process STDOUT/STDERR
    
        cfg                                 # The configuration files for the run
    
            environment.txt                 # Master process environment variable list
            harness.yaml                    # ist.yaml
            parameter.yaml                  # -p from the command line
            testbed.yaml                    # -t from the command line
            suite.yaml                      # -s from the command line
    
        harness.log                         # Master process STDOUT/STDERR
        results.log                         # The Sub-process results summary
        
CONFIGURATION FILES:

    Example configuration files are provided, with comments:
    
        .../its/parametercfg/EXAMPLE.yaml
        .../its/testbedcfg/EXAMPLE.yaml
        .../its/suitecfg/EXAMPLE.yaml

REFERENCE:

    https://www.youtube.com/watch?v=pq1SZrZbRMA
"""

import os, sys, yaml

os.umask(000)

if __name__ != '__main__':
    print __doc__
    os._exit(0)

# Where are we (pwd)?  Add the lib directory to the python path
baseDir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )
sys.path.append( os.path.join( baseDir, 'lib' ) )

import ItsCliArguments, ItsCfg
import ItsTestbed, ItsRunner, ItsLogger
import ItsReservationController

# Process CLI arguments
args = ItsCliArguments.ItsCliArguments()
#print args.toString()

# Show arguments
if args.verbose > 0:
    print args.toString(),
# Show ITS pydoc documentation
if args.help:
    print __doc__
    os._exit(0)

# Process configuration files
cfg = ItsCfg.ItsCfg( args, baseDir )
cfg.parseFiles()
#print cfg.toString()
    
# Run a test
if args.action == "run":
    
    # Parse the Testbed and instantiate the server objects
    testbed = ItsTestbed.ItsTestbed( cfg, baseDir )
    testbed.makeServers()
    #testbed.validate( args )   ### Reservations not enabled.
    
    # Build the test list
    runner = ItsRunner.ItsRunner( cfg, testbed )
    runner.buildTestList()
    
    # Prepare the directories and logs
    logger = ItsLogger.ItsLogger( runner, cfg )
    logger.prepLogs()
    
    # Handle Cntl-C
    runner.signals.logger = logger
    runner.registerSignalHandlers()
    
    # Execute the tests
    runner.run()

    sys.exit( runner.testSuite.rc )

# Do reservations
else:

    path = ItsReservationController.ItsReservationController( cfg, args ).do()
    if args.action == 'reserve':
        if len( path ):
            print path
        else:
            sys.exit( 1 )

sys.exit( 0 )




















