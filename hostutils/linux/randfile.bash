#!/bin/bash

# randfile.bash <targetdir> <smallest> <largest>
# randfile.bash /usr 1k 512k

#-size n[cwbkMG]
#       File uses n units of space.  The following suffixes can be used:
#       `b'    for 512-byte blocks (this is the default if no suffix is used)
#       `c'    for bytes
#       `w'    for two-byte words
#       `k'    for Kilobytes (units of 1024 bytes)
#       `M'    for Megabytes (units of 1048576 bytes)
#       `G'    for Gigabytes (units of 1073741824 bytes)

Target=$1
Lower=$2
Upper=$3
File=""

function get_file {
	
	# A directory was specified; choose a random file recursively below it
	if [[ -d $Target ]]
	then
        f=`find $Target -type f -size +$Lower -a -size -$Upper | grep -v '\s' | sort -R | head -1`
    fi
	
	echo $f
}

for i in `seq 1 10`
do
    File=$(get_file)
    if [[ ! -d $File && -e $File ]]
    then
        break
    fi	
done

if [[ -e $File ]]
then
    size=$(stat --printf="%s" "$File")
    echo $File $size 
else
    exit 1
fi
