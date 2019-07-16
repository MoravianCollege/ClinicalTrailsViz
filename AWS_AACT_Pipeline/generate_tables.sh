#!/bin/bash

#The hostname is received from get_database_data.sh
#hostname=$1
hostname='clinicaltrialstestserver.cfdgyctoflg4.us-east-2.rds.amazonaws.com'

python3 sponsor_type.py "$hostname"

python3 condition_type.py "$hostname"
