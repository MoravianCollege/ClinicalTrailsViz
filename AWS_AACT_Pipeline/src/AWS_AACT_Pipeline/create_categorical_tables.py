#!/usr/bin/env python
from dotenv import load_dotenv
import boto3
import os
import subprocess

try:
    load_dotenv()
    DBInstanceIdentifier = os.getenv('DBInstanceIdentifier')

    # Create RDS database instance
    rds = boto3.client('rds')

    index = 0

    # get all of the db instances and find index of our instance
    dbs = rds.describe_db_instances()
    for db in dbs['DBInstances']:
        if dbs['DBInstances'][index]['DBInstanceIdentifier'] == DBInstanceIdentifier:
            break
        else:
            index = index + 1

    hostname = dbs['DBInstances'][index]['Endpoint']['Address']

    # Get path to generate_tables.sh file and pass hostname
    file_path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))
    data_path = os.path.join(project_path, 'AWS_AACT_Pipeline/scripts/generate_tables.sh')
    subprocess.call(['bash', data_path, hostname])

except Exception as error:
    print(error)
