#!/bin/bash

# ./s3file.bash 

S3Config=$1
Bucket=$2
Target=$3
File=$Target
S3cmd=$4

# The source file
if [[ -d $Target ]]
then
    File=$(./randfile.bash $Target)
fi

if [[ -z $S3cmd ]]
then
    S3cmd='/root/hostutils/linux/s3cmd-1.6.1/s3cmd-1.6.1/s3cmd'
fi

echo SOURCE $File

Basename=$(basename $File)
Hostname=`hostname --fqdn`
Name=$Basename-$Hostname-$$

# Put a file
echo "Putting File" $Basename "as" $Name
dd if=$File | tee >(md5sum > /tmp/$Name.md5) | $S3cmd -c $S3Config put - s3://$Bucket/$Name

# Get the file
echo "Getting File" $Basename "as" $Name
$S3cmd -c $S3Config get s3://$Bucket/$Name - 2>/dev/null | md5sum > /tmp/$Name-get.md5

# Check the gotten file against its original md5sum
echo "Diffing md5sums"
diff /tmp/$Name.md5 /tmp/$Name-get.md5

if [[ $? -ne 0 ]]
then
    echo "CORRUPTION FOUND; Exiting"
    exit 1
else
    echo "md5sum okay"
fi

rm -f /tmp/$Basename.md5 /tmp/$Basename-get.md5

