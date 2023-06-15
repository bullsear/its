#!/bin/bash

if [ $# -lt 4 ]
then
    echo "ERROR: 4 arguments are required by ssh.bash"
    exit 1
fi

username=$1
shift
password=$1
shift
server=$1
shift
from=$1
shift
to=$1

#echo $username
#echo $password
#echo $server
#echo $from
#echo $to

greprc=$( grep $server ~/.ssh/known_hosts > /dev/null; echo $? )
if [[ "$greprc" != 0 ]]
then
    #echo Adding Host $server to ~/.ssh/known_hosts
    ssh-keyscan $server >> ~/.ssh/known_hosts 2>/dev/null
fi

#/mnt/its/its/bin/sshpass -p $password scp -r $username@$server:$from $to 2>&1
$ITS_BASEDIR/bin/sshpass -p $password scp -r $from $username@$server:$to 2>&1

#rc=$?
#
#echo rc=$rc
#
#exit $rc

