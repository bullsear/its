"""ItsCliArguments.py - ITS Harness Arguments
NAME:
    ItsCliArguments.py - ITS Harness Arguments
"""

import os, sys, getopt, ItsException
import __main__ as main

class ItsCliArguments ( object ):
    
    #$> its -a run -p <path>/parametercfg.yaml -t <path>/testbedcfg.yaml -s <path>/suitecfg.yaml
    #$> its -a run -t <path>/testbedcfg.yaml -s <path>/suitecfg.yaml    
    #
    #$> reserve.py -a reserve -y skyera -c 40G-1 -u tshoenfelt -n 30
    #$> reserve.py -a unreserve -r 90c79b4265414a3bb60701bf1991387f
    #$> reserve.py -a update -r 90c79b4265414a3bb60701bf1991387f -n 60
    #$> reserve.py -a showreservation -r 90c79b4265414a3bb60701bf1991387f
    #$> reserve.py -a showallreservations
    #$> reserve.py -a showtypes
    #$> reserve.py -a showpools
    #$> reserve.py -a showall    
    
    def __init__ ( self, pop=True ):
        if pop:
            sys.argv.pop( 0 )
            
        self.action             = ""      # -a    action (reserve|unreserve|show|list|run)
        
        # Reservations
        self.type               = ""      # -y    testbed type
        self.file               = ""      # -f    file path to existing reserved testbed descriptor
        self.pool               = ""      # -c    connection pool
        #self.suite              = ""      # -s    a test suite
        self.user               = ""      # -u    username
        self.duration           = ""      # -n    reservation duration
        self.email              = ""      # -e    user email address
        self.reserveId          = ""      # -g    existing reservation id
        self.verbose            = 0       # -v    verbosity level
        self.iterations         = 1       # -i    how many times to poll for a reservation
        self.sleep              = 10      # -e    how long to sleep between reservation polls, in seconds
        
        # Run
        self.parametercfgfile   = ""      # -p    parameter config
        self.testbedcfgfile     = ""      # -t    testbed config
        self.suitecfgfile       = ""      # -s    test suite config
        self.nocheck            = False   # -x    don't check testbed ssh before executing tests
        self.subject            = ""      # -b    add a string to the email subject (to help filtering)
        
        self.help               = False   # -h    show help and exit            
        
        try:
            opts, args = getopt.getopt( sys.argv, "a:y:c:s:u:n:e:g:v:i:e:p:t:s:b:xh" )
        except getopt.GetoptError:
            print "ERROR: Incorrect command line options (-h for help)"
            sys.exit(2)

        if not opts:
            self.help = True
            return

        for opt, arg in opts:
            
            if opt in ( "-a" ):
                self.action = arg            
            elif opt in ( "-y" ):
                self.type = arg
            elif opt in ( "-f" ):
                self.file = arg
            elif opt in ( "-c" ):
                self.pool = arg
            #elif opt in ( "-s" ):
            #    self.suite = arg
            elif opt in ( "-u" ):
                users = arg.split(",")
                self.user = users[0]
                emails = []
                for u in users:
                    emails.append( u + "@hgst.com" )
                self.email = ','.join( emails )
            elif opt in ( "-n" ):
                self.duration = arg                
            elif opt in ( "-g" ):
                self.reserveId = arg
            elif opt in ( "-v" ):
                self.verbose = int( arg )
            elif opt in ( "-i" ):
                self.iterations = arg   
            elif opt in ( "-e" ):
                self.sleep = arg
            elif opt in ( "-p" ):
                self.parametercfgfile = arg
            elif opt in ( "-t" ):
                self.testbedcfgfile = arg
            elif opt in ( "-s" ):
                self.suitecfgfile = arg
            elif opt in ( "-x" ):
                self.nocheck = True
            elif opt in ( "-b" ):
                self.subject = arg
            elif opt in ( "-h" ):
                self.help = True   
            else:
                pass
            
        try:
            self.checkArgs()
        except ItsException.ItsUsageException as e:
            print e
            print
            print main.__doc__
            sys.exit( 255 )
            
    def checkArgs ( self ):
        
        if self.help:
            return
        
        #if self.verbose > 0:
        #    print self.toString()
        
        self.checkAction()
        
        if self.action == 'run':
            self.checkRun()
        else:
            self.checkReserve()
    
    def checkAction( self ):
        allActions = [ 'run', 'reserve', 'unreserve', 'update', 'showreservation', 'showallreservations', 'showtypes', 'showpools', 'showall' ]
        if len( self.action ) == 0:
            self.usageException( "Action -a argument required." )
        if self.action not in allActions:
            self.usageException( "Action -a must be one of: " + ", ".join( allActions ) )
    
    def checkRun( self ):
        #$> its -a run -y <path>/testbedcfg.yaml -s <path>/suitecfg.yaml
        if self.testbedcfgfile == "" or self.suitecfgfile == "" or self.user == "":
            self.usageException( "Action -a 'run' requires -t (testbed), -s (test suite), and -u (username) flags" )
        if not os.path.isfile( self.testbedcfgfile ):
            self.usageException( "Can't find testbed config file: " + self.testbedcfgfile )            
        if not os.path.isfile( self.suitecfgfile ):
            self.usageException( "Can't find suite config file." + self.suitecfgfile )            
        if os.path.basename( self.parametercfgfile ) == "EXAMPLE.yaml" \
            or os.path.basename( self.testbedcfgfile ) == "EXAMPLE.yaml" \
            or os.path.basename( self.suitecfgfile ) == "EXAMPLE.yaml":
                self.usageException( "Using EXAMPLE.yaml config files prohibited." )            
    
    def checkReserve( self ):
        if self.action == 'reserve':
            # We know what we want
            #$> its.py -a reserve -y skyera -c 40G-1 -u tshoenfelt -n 30
            if ( len( self.suitecfgfile ) == 0 ):
                if ( ( len( self.type ) == 0 or len( self.pool ) == 0 ) or len( self.user ) == 0 or len( self.duration ) == 0 ):
                    self.usageException( "Action -a 'reserve' requires -y (type), -c (pool), -u (user), and -n (duration) arguments." )
            # Auto-provision
            #$> its.py -a reserve -s /mnt/its/its/tests/fio1.yaml -u tshoenfelt -n 30
            else:
                if ( len( self.user ) == 0 or len( self.duration ) == 0 or len( self.suitecfgfile ) == 0 ):
                    self.usageException( "Action -a 'reserve' requires -s (suite), -u (user), and -n (duration) arguments"  )            
        #$> its.py -a unreserve -r 90c79b4265414a3bb60701bf1991387f
        elif self.action == 'unreserve':
            if ( len( self.reserveId ) == 0 ):
                self.usageException( "Action -a 'unreserve' requires the -g (reserve id) argument." )
        #$> its.py -a update -r 90c79b4265414a3bb60701bf1991387f -n 60
        elif self.action == 'update':
            if ( len( self.reserveId ) == 0 ):
                self.usageException( "Action -a 'update' requires the -g (reserve id) argument." )
        #$> its.py -a showreservation -r 90c79b4265414a3bb60701bf1991387f
        elif self.action == 'showreservation':
            if ( len( self.reserveId ) == 0 ):
                self.usageException( "Action -a 'showreservation' requires the -g (reserve id) argument." )
        #$> its.py -a showallreservations
        #$> its.py -a showtypes
        #$> its.py -a showpools
        #$> its.py -a showall        
    
    def usageException( self, mesg ):
        print self.toString(),
        print "INCORRECT USAGE"
        raise ItsException.ItsUsageException( mesg )       
        
    def toString ( self ):
        s = "=" * 65 + "\n"
        s += "                           ARGUMENTS\n"
        s += "Action                : " + self.action + "\n"
        s += "Type                  : " + self.type + "\n"
        s += "User                  : " + self.user + "\n"
        s += "Pool                  : " + self.pool + "\n"
        s += "Duration              : " + self.duration + "\n"
        s += "Email                 : " + self.email + "\n"
        s += "ID                    : " + self.reserveId + "\n"
        s += "Verbosity             : " + str( self.verbose ) + "\n"
        s += "Iterations            : " + str( self.iterations ) + "\n"
        s += "Sleep                 : " + str( self.sleep ) + "\n"
        s += "Help                  : " + str( self.help ) + "\n"
        s += "Email Subject         : " + str( self.subject ) + "\n"
        s += "Parameter Config File : " + str( self.parametercfgfile ) + "\n"
        s += "Testbed Config File   : " + str( self.testbedcfgfile ) + "\n"
        s += "Suite Config File     : " + str( self.suitecfgfile ) + "\n"
        s += "No Check Testbed ssh  : " + str( self.nocheck ) + "\n"
        s += "=" * 65 + "\n"        
        return s        
        
    