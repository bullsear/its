#!/usr/bin/env python

"""testrail_results.py - Post ITS Run Results to Testrail
NAME:

    testrail_results.py - Post ITS Run Results to Testrail

SYNOPSIS:

    $> ./testrail_results.py -i <testrailrunid> -d <pathtoitsrundir> -u <testrailuser> -p <testrailpassword>

ARGUMENTS:

    -i = Testrail test run id
    -d = File system path to the ITS test run directory
    -u = Testrail user id, usually an email address
    -p = Testrail password

DESCRIPTION:

    This script uploads all the test results from an ITS suite run to a Testrail
    test run.  It records the upload with each test's ITS test logs in a the
    testrail.yaml file.

REFERENCE:

    https://www.youtube.com/watch?v=pq1SZrZbRMA
"""

import os, sys, yaml

if __name__ != '__main__':
    print __doc__
    os._exit(0)
    
# Where are we (pwd)?  Add the lib directory to the python path
baseDir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )
sys.path.append( os.path.join( baseDir, 'lib' ) )

# Add the TestRail directory to the search path
sys.path.append( os.path.join( baseDir, 'lib/TestRail/testrail-api-master/python/2.x' ) )

import ItsTestRailArguments, ItsException

args = ItsTestRailArguments.ItsTestRailArguments()

# Show arguments
if int( args.verbose > 0 ):
    print args.toString(),
# Show ITS pydoc documentation
if args.help:
    print __doc__
    os._exit(0)

try:
    args.checkArgs()
except ItsException.ItsUsageException as e:
    print "USAGE ERROR: ",
    print e
    print "YOUR COMMAND: " + " ".join( sys.argv )
    sys.exit( 255 )
            
from testrail import *
from pprint import *

# Find files
def findAll ( name, path, justOne=False ):
    found = []
    for root, dirs, files in os.walk( path ):
        if name in files:
            path = os.path.join( root, name )
            found.append( path )
            if justOne:
                break
    return found

def findTestRailTest ( tests, testrailCaseId ):
    #print testrailCaseId
    test = False
    for t in tests:
        #print t['case_id']
        if int( t['case_id'] ) == int( testrailCaseId ):
            test = t
    return test

# Find the run meta data
runMeta = findAll( 'run.yaml', args.runDir )

print "Found this metadata file:\n"
print runMeta[0], "\n"

metaYaml = yaml.load( file( runMeta[0], 'r' ) )
if int( args.verbose ) > 0:
    print metaYaml

# Find the test results
files = findAll( 'meta.log', args.runDir )
files.sort()

# Get ready to talk to Testrail
testRailBaseUrl = 'http://sqatest8.hgst.com/testrail'
testRailClient = APIClient( testRailBaseUrl )
testRailClient.user = args.user
testRailClient.password = args.password

# Find the tests in the Testrail run
runTests = testRailClient.send_get( '/'.join( [ 'get_tests', args.testrailRunId ] ) )
if int( args.verbose ) > 0:
    print "Testrail tests in run: " + args.testrailRunId
    pprint( runTests )

print "Found these ITS results:\n"
#pprint( files )
                
resultsMap = {
    'UNKNOWN' : 4, # 'Retest'
    'PASS' : 1,
    'FAIL' : 5,
}

# Post the results
for f in files:
    print f
    d = os.path.dirname( f )
    myYaml = yaml.load( file( f, 'r' ) )
    #pprint( myYaml )
    testrailCaseId = myYaml['id']
    elapsed = 'Unknown'
    try:
        elapsed = int( float ( myYaml['duration'] ) )
    except:
        pass
    #itsRun = pformat( metaYaml )
    comment = '\n'.join(
        [
        "ITS Run Details:\n",
        "Hostname: " + metaYaml['hostname'],
        "Run ID: " + metaYaml['runId'],
        "Log Directory: " + metaYaml['runDir'],
        "Run URL: " + metaYaml['runURL'],
        "Run User Email: " + metaYaml['useremail'],
        ]
    )
    params = {
        'comment' : comment,
        'elapsed' : str( elapsed ) + 's',
        'status_id' : resultsMap[myYaml['result']]
    }
    print "Testrail Run ID: " + args.testrailRunId
    print "Testrail Test ID: " + testrailCaseId
    if int( args.verbose ) > 0:
        print params
 
    print "POSTING RESULT TO TESTRAIL"
    results = ''
    # Try using the mapped id from the suite id for the testrail test case id
    try:
        results = testRailClient.send_post( '/'.join( [ 'add_result_for_case', args.testrailRunId, testrailCaseId ] ), params )
    except Exception as e:
        print "Unable to post result for test: " + testrailCaseId

    # Try using the script name for the testrail test case id
    if len( results ) == 0:
        try:
            testScriptName = myYaml['testInstanceId'].split( '_' )[2].lstrip( 'C' )
            results = testRailClient.send_post( '/'.join( [ 'add_result_for_case', args.testrailRunId, testScriptName ] ), params )
        except Exception as e:
            print "Unable to post result for test: " + testScriptName
            print
            continue
        
    results['resultsCaseUrl'] = '/'.join( [ testRailBaseUrl, 'index.php?/tests/view', str( results['test_id'] ) ] )
    
    if int( args.verbose ) > 0:
        print
        print "POST RESULTS:"
        pprint( results )
    #yaml.dump( results, file( os.path.join( d, 'testrail.yaml' ), 'w' ), default_flow_style=False )
    yaml.safe_dump( results, file( os.path.join( d, 'testrail.yaml' ), 'w' ), encoding='utf-8', allow_unicode=False, default_flow_style=False )
    
    # testRailRunTest = findTestRailTest( runTests, testrailCaseId )
    # pprint( testRailRunTest )   
    
    print
        
# cases = testRailClient.send_get( '/'.join( [ 'get_run', args.testrailRunId ] ) )
# pprint( cases )

# runTests = testRailClient.send_get( '/'.join( [ 'get_tests', args.testrailRunId ] ) )
# pprint( runTests )


    