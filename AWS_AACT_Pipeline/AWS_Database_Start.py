#!/usr/bin/env python
import boto3
import os
import time
import subprocess

DBName = os.getenv('DBName')
DBInstanceIdentifier = os.getenv('DBInstanceIdentifier')
MasterUsername = os.getenv('MasterUsername')
MasterUserPassword = os.getenv('MasterUserPassword')

# Create RDS database instance
rds = boto3.client('rds')


try:
    response = rds.create_db_instance(
        DBName=DBName,
        DBInstanceIdentifier=DBInstanceIdentifier,
        MasterUsername=MasterUsername,
        MasterUserPassword=MasterUserPassword,
        DBInstanceClass='db.m4.large',
        Engine='postgres',
        AllocatedStorage=20,
        Port=5432)
    print(response)
except Exception as error:
    print(error)


index = 0

# get all of the db instances and find index of our instance
dbs = rds.describe_db_instances()
for db in dbs['DBInstances']:
    print(db)
    if dbs['DBInstances'][index]['DBInstanceIdentifier'] == DBInstanceIdentifier:
        break
    else:
        index = index + 1

# wait until instance is available to get address and populate database
try:
    while True:
        if dbs['DBInstances'][index]['DBInstanceIdentifier'] == DBInstanceIdentifier and \
                dbs['DBInstances'][index]['DBInstanceStatus'] == 'available':
            hostname = dbs['DBInstances'][index]['Endpoint']['Address']
            f = open(os.path.expanduser('~/.bash_profile'), 'a')
            f.write("export hostname=" + hostname)
            f.close()
            break
        else:
            print("Sleeping...")
            time.sleep(5)
            dbs = rds.describe_db_instances()
except Exception as error:
    print(error)

subprocess.call("./get_database_data.sh")
