#!/usr/bin/env python

"""resnag.py - Send Email reminders to Reservation System Users
NAME:
    resnag.py - Send Email reminders to Reservation System Users
"""

import os, sys, yaml, time, re, shutil, commands, datetime

if __name__ != '__main__':
    print __doc__
    os._exit(0)
    
# Where are we (pwd)?
baseDir = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )
sys.path.append( os.path.join( baseDir, 'lib' ) )

import ItsHarnessCfg, ItsReservationDatabase, ItsTime, ItsMail, ItsReservation

# Parse the configs 
harnessCfg = ItsHarnessCfg.ItsHarnessCfg( os.path.join( baseDir, 'cfg', 'harnesscfg', 'its.yaml' ) )
harnessCfg.parseFile()
#print harnessCfg.toString()

resRootDir = harnessCfg.yaml['ITS_RESERVATION_DIR']

#dirs = os.listdir( resRootDir )
#print dirs

reservationsDir = os.path.join( resRootDir, 'reservations', 'reservations' )
#print reservationsDir

reservations = os.listdir( reservationsDir )
#print resDirs

#{
#   'file': '/mnt/its/its/reserve/reservations/testbeds/f4a20ff9bede46c69b9c37e7de9a101e.yaml',
#   'testbed': [{'username': 'root', 'password': 'password', 'type': 'linux_centos_6.3_intel_64bit', 'server': 'localhost'}],
#   'db': '',
#   'user': 'todd.shoenfelt',
#   'startTime': '2015-08-10 12:59:45.222196',
#   'duration': '30',
#   'endTime': '',
#   'type': 'testbed',
#   'id': 'f4a20ff9bede46c69b9c37e7de9a101e',
#   'pool': '40G-1',
#   'reservationFile': '/mnt/its/its/reserve/reservations/reservations/f4a20ff9bede46c69b9c37e7de9a101e.yaml'
#}

for r in reservations:

    #pass
    path = os.path.join( reservationsDir, r )
    #print path
    myYaml = yaml.load( file( path, 'r' ) )
    
    reservation = ItsReservation.ItsReservation()
    reservation.thaw( myYaml['id'], reservationsDir )
    #print reservation.toString()    
#************ RESERVATION *************
#duration: '30'
#endTime: ''
#file: /mnt/its/its/reserve/reservations/testbeds/f4a20ff9bede46c69b9c37e7de9a101e.yaml
#id: f4a20ff9bede46c69b9c37e7de9a101e
#pool: 40G-1
#reservationFile: /mnt/its/its/reserve/reservations/reservations/f4a20ff9bede46c69b9c37e7de9a101e.yaml
#startTime: '2015-08-10 12:59:45.222196'
#testbed:
#- password: password
#  server: localhost
#  type: linux_centos_6.3_intel_64bit
#  username: root
#type: testbed
#user: todd.shoenfelt

    #print yaml      # Ok
    durationSeconds = int( myYaml['duration'] ) * 60
    #print durationSeconds
    startDate, startTime = myYaml['startTime'].split( " " )
    #print startDate, startTime
    startYear, startMonth, startDay = startDate.split( '-' )
    #print startYear, startMonth, startDay
    startHour, startMinutes, startSecondsFloat = startTime.split( ':' )
    startSeconds, startMicroSeconds = startSecondsFloat.split( '.' )
    #print startDate, startTime, startYear, startMonth, startDay, startHour, startMinutes, startSeconds, startMicroSeconds
    
    startEpoch = datetime.datetime( int(startYear), int(startMonth), int(startDay), int(startHour), int(startMinutes), int(startSeconds), int(startMicroSeconds) ).strftime( '%s' )
    #print startEpoch

    nowEpoch = int( time.time() )
    due = int( startEpoch ) + int( durationSeconds )
    #print due
    #print nowEpoch, due
    
    overdue = nowEpoch - due
    #print overdue

    if overdue > 0:
        msg = myYaml['id'] + ' overdue by ' + str( overdue ) + ' seconds, reserved by ' + myYaml['user'] 
        print msg
        mail = ItsMail.ItsMail()
        mail.mailTo = myYaml['user'] + '@hgst.com'
        mail.subject = 'ITS Overdue Reservation ' + myYaml['id']
        mail.text = msg + "\n\n" + reservation.toString() 
        mail.send()
    else:
        print myYaml['id'] + ' not overdue'
        
    
        
        
        
        
        