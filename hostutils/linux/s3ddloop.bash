#!/bin/bash

Iterations=$1
BlockSize=$2
Count=$3
S3Config=$4
Bucket=$5
ChunkSize=$6
Dev=$7
MaxSize=$8
S3cmd=$9

if [[ -z $S3cmd ]]
then
    S3cmd='/root/hostutils/linux/s3cmd-1.6.1/s3cmd-1.6.1/s3cmd'
fi

echo Planned $Iterations Iterations

echo =====================================

for i in `seq 1 $Iterations`
do

	echo ITERATION $i

    # Check the total bucket size
    if [[ ! -z $MaxSize ]]
    then
        echo "Bucket Size"
        $S3cmd -c $S3Config du s3://$Bucket
    fi
    
    # Write a file
    ./s3ddfile.bash $BlockSize $Count $S3Config $Bucket $ChunkSize $Dev $S3cmd
    
    if [[ $? -ne 0 ]]
    then
        exit 1
    fi

	echo -----------------------------------------------------------

done

