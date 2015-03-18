#!/bin/bash
#usage ./calc.sh before_calc
# this should get moved to a native gnuplot function
TMP=./.delme
while read line; do
    lbs=$(echo $line | awk {'print $2'})
    if [ ! -z "$lbs" ];
    then
       echo "$line" >> $TMP 
    fi
done < $1
tac $TMP | gawk 'NR==1 {sum=$2; lambda=.9; print $1,$2,sum,$3} ; NR>1 {sum=lambda*sum+(1-lambda)*$2; print $1,$2,sum,$3}'
rm $TMP
