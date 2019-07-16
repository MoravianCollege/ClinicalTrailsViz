#!/bin/bash

#hostname received from create_categorical_tables.py
hostname=$1

python3 src/AWS_AACT_Pipeline/sponsor_type.py "$hostname"

python3 src/AWS_AACT_Pipeline/condition_type.py "$hostname"
