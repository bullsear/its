#!/bin/bash

if [ $# -lt 4 ]
then
    echo "ERROR: 5 arguments are required by ssh.bash"
    exit 1
fi

itsprocess=$1
#shift
username=$2
#shift
password=$3
#shift
server=$4
#shift
#munge=$1
#shift
###command=$@
command=$5

ITS_BASEDIR=`dirname $0`

#echo $itsprocess
#echo $username
#echo $password
#echo $server
#echo $command
#echo $fullcommand

# $command must be quoted if it contains pipes, semi-colons, or redirects   

# Increase the server connections
#[root@todd4 tshoenfelt]# grep Max /etc/ssh/sshd_config | grep 200
#MaxSessions 200
#MaxStartups 200

#greprc=$( grep $server ~/.ssh/known_hosts > /dev/null; echo $? )
#if [[ "$greprc" != 0 ]]
#    ### Experimental
#    # Replace the key
#    ssh-keygen -f "~/.ssh/known_hosts" -R $server
#then
#    #echo Adding Host $server to ~/.ssh/known_hosts
#    ssh-keyscan $server >> ~/.ssh/known_hosts 2>/dev/null
#fi
#check_ssh.bash $ITS_BASEDIR $username $password $server

# For transferring a file
#sshpass -p password scp root@localhost:/tmp/ls.from /tmp/ls.to

#/mnt/its/its/bin/sshpass -p$password ssh $username@$server $command 2>&1
#ITS_BASEDIR=`dirname $0`
#$ITS_BASEDIR/sshpass -p$password ssh $username@$server $command 2>&1
$ITS_BASEDIR/sshpass -p$password ssh $username@$server "export ITS_HOST_PID=$itsprocess; $command" 2>&1
rc=$?
#echo $?
if [[ "$rc" == 255 ]]
then
    $ITS_BASEDIR/check_ssh.bash $ITS_BASEDIR $username $password $server
    $ITS_BASEDIR/sshpass -p$password ssh $username@$server "export ITS_HOST_PID=$itsprocess; $command" 2>&1
    rc=$?
    echo $exCode
fi
exit $rc
# This is the remote return code
#rc=$?
#
#echo rc=$rc
#
#exit $rc

