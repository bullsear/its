#!/bin/bash

username=$2
#shift
password=$3
#shift
server=$4

greprc=$( grep $server ~/.ssh/known_hosts > /dev/null; echo $? )

# The host is known, but the key may be incorrect
if [[ "$greprc" != 0 ]]
then
    # Remove the key
    echo REMOVING KEY FOR $server
    ssh-keygen -f "~/.ssh/known_hosts" -R $server
fi

echo ADDING KEY FOR $server
ssh-keyscan $server >> ~/.ssh/known_hosts 2>/dev/null


