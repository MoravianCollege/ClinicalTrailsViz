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

    subprocess.call(['bash', 'scripts/generate_tables.sh', hostname])

except Exception as error:
    print(error)
