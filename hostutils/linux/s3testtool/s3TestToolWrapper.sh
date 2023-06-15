#!/bin/bash

BUCKET=$1
BQ=$[$2+1]
FQ=$3
FSIZE=$4
THREADS=$5
DEL=$6
COUNT=1

if [ ! "$BUCKET" ] || [ ! "$BQ" ] || [ ! "$FQ" ] || [ ! "$THREADS" ] || [ ! "$FSIZE" ]; then
  echo "Requires Arg1 to bucket name"
  echo "Arg2 to be # of buckets"
  echo "Arg3 to be # of files/bucket"
  echo "Arg4 to be file size in bytes"
  echo "Arg5 to be # of threads"
  echo "Optional - any 6th arg will be considered delete all when done"
 
  exit
fi


while [ $COUNT -lt $BQ ]
do

    java -jar ./S3TestTool.jar PUT -a AK0ETY72AQAQ5GR63RCV -s ZeJ3OOrHm6UDQkAXsDfmqlYaF2p90k3qiFSqWjVG -e http://192.168.1.11:80,http://192.168.1.12:80,http://192.168.1.13:80,http://192.168.2.11:80,http://192.168.2.12:80,http://192.168.2.13:80 -S $FSIZE -t $THREADS -n $FQ -r10 -b $BUCKET$COUNT
    COUNT=$((COUNT+1))

done

DELCOUNT=$2
echo "The delete count is "$DELCOUNT
LOOPCOUNT=1
if [ ${DEL+"true"} ]; then
  for ((c=1; c<=$DELCOUNT; c++ )); do
    s3cmd -c cfg.scaler1-ip1 del s3://$BUCKET$LOOPCOUNT --recursive --force|wc
    echo "s3cmd -c cfg.scaler1-ip1 del s3://$BUCKET$LOOPCOUNT --recursive --force|wc"
    LOOPCOUNT=$((LOOPCOUNT+1))
  done
fi
