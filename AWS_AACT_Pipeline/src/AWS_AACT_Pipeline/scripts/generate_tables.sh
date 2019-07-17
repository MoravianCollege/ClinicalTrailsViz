#!/bin/bash

#hostname received from create_categorical_tables.py
hostname=$1

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
echo ${parent_path}
cd ${parent_path}

python3 ../sponsor_type.py "$hostname"

python3 ../categorize_driver.py "$hostname"
