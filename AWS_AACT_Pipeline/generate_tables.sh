#!/bin/bash

#hostname received from create_categorical_tables.py
hostname=$1

python3 sponsor_type.py "$hostname"

python3 condition_type.py "$hostname"
