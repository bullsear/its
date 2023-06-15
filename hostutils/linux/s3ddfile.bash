#!/bin/bash

# ./s3ddfile.bash <blocksize> <blockcount> <path-to-s3-config> <existing-bucket> (urandom|zero) <path-to-s3cmd>

BlockSize=$1
Count=$2
S3Config=$3
Bucket=$4
ChunkSize=$5
Dev=$6
S3cmd=$7

if [[ -z $S3cmd ]]
then
    S3cmd='/root/hostutils/linux/s3cmd-1.6.1/s3cmd-1.6.1/s3cmd'
fi

# Create a unique file name
Basename=`uuidgen`
echo "Putting File" $Basename	    

# Stream a put and compute the md5sum inline
#dd if=/dev/$Dev bs=$BlockSize count=$Count | tee >(md5sum > /tmp/$Basename.md5) | $S3cmd -c $S3Config --multipart-chunk-size-mb=$ChunkSize put - s3://$Bucket/$Basename
dd if=/dev/$Dev bs=$BlockSize count=$Count | tee >(md5sum > /tmp/$Basename.md5) | $S3cmd -c $S3Config put - s3://$Bucket/$Basename

# Stream the file get and compute the md5sum inline
echo "Getting File" $Basename	
$S3cmd -c $S3Config get s3://$Bucket/$Basename - 2>/dev/null | md5sum > /tmp/$Basename-get.md5

# Check the gotten file against its original md5sum
echo "Diffing md5sums"
diff /tmp/$Basename.md5 /tmp/$Basename-get.md5

if [[ $? -ne 0 ]]
then
    echo "CORRUPTION FOUND; Exiting"
    exit 1
else
    echo "md5sum okay"
fi

rm -f /tmp/$Basename.md5 /tmp/$Basename-get.md5

