#!/usr/bin/env python
from dotenv import load_dotenv
import boto3
import os
import time
import subprocess

try:
    load_dotenv()
    DBName = os.getenv('Temp_DBName')
    DBInstanceIdentifier = os.getenv('DBInstanceIdentifier')
    MasterUsername = os.getenv('MasterUsername')
    MasterUserPassword = os.getenv('MasterUserPassword')
    DBPort = os.getenv('DBPort')

    # Create RDS database instance
    rds = boto3.client('rds')

    response = rds.create_db_instance(
        DBName=DBName,
        DBInstanceIdentifier=DBInstanceIdentifier,
        MasterUsername=MasterUsername,
        MasterUserPassword=MasterUserPassword,
        DBInstanceClass='db.m4.large',
        Engine='postgres',
        AllocatedStorage=20,
        Port=int(DBPort))

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
                break
            else:
                print("Waiting for new instance to become available...")
                time.sleep(15)
                dbs = rds.describe_db_instances()
    except Exception as error:
        print("Cannot locate database index:", error)

    hostname = dbs['DBInstances'][index]['Endpoint']['Address']
    subprocess.call(['bash', './get_database_data.sh', hostname, DBPort, MasterUsername, DBName])

except Exception as error:
    print(error)


