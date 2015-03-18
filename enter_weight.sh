#!/bin/bash
if [ -z $1 ]; 
then
    echo "USAGE: ./enter_days.sh <start-n-days-back>";
    exit 1;
fi
    echo `date -d "now - $1 day" -I `
    for i in $(seq 0 $1); do read lbs; echo `date -d "now - $i day" -I` $lbs | tee -a self_data; done
