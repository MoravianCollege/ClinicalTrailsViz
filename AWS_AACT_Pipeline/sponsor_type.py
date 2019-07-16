# coding=utf-8
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import re
import sys

df = pd.DataFrame

try:
    # load information from .env file to log in and connect to the database
    load_dotenv()
    MasterUsername = os.getenv('MasterUsername')
    MasterUserPassword = os.getenv('MasterUserPassword')
    hostname = sys.argv[1]
    DBName = os.getenv('DBName')
    DBPort = os.getenv('DBPort')

    # Connect to database
    connection = psycopg2.connect(
        user=MasterUsername,
        password=MasterUserPassword,
        host=hostname,
        database=DBName,
        port=DBPort)

    cursor = connection.cursor()

    # initiated variables to create the new column
    sql_command = "SELECT nct_id, name FROM ctgov.sponsors"
    new_column_name = 'sponsor_category'

    # retrieve wanted data from the query (in the form of a data frame)
    df = pd.read_sql_query(sql_command, con=connection)

    # check conditions_list.txt to determine the value to be assigned for the row in the new column
    df[new_column_name] = np.where(
        df.name.str.contains("college|school|univers|higher education|academy", flags=re.IGNORECASE, ), "Education",
        np.where(df.name.str.contains('hospital|hopit|hospice|hôpitaux', flags=re.IGNORECASE), "Hospitals",
        np.where(df.name.str.contains('pharmac', flags=re.IGNORECASE), "Pharmaceuticals",
        np.where(df.name.str.contains('research|laborator', flags=re.IGNORECASE), "Research Teams",
        np.where(df.name.str.contains('institu|istituto', flags=re.IGNORECASE), 'Institutions',
        np.where(df.name.str.contains('center|centre|centro|group|medicine|health|medical|clinic', flags=re.IGNORECASE), 'Medicine & Health',
        np.where(df.name.str.contains('foundation|fund|fondation|fondazione', flags=re.IGNORECASE), "Foundations",
        np.where(df.name.str.contains(' inc |inc\\.|co\\.|company|corpor|corp\\.|incorporated|ltd\\.|llc\\.|ltd| inc| llc', flags=re.IGNORECASE), 'Companies',
        np.where(df.name.str.contains('united states|government', flags=re.IGNORECASE), 'Government', "Other")))))))))

    df.drop('name', axis=1, inplace=True)

    # Create a directory for csv information if it doesn't exist yet
    if not os.path.exists('csv_scripts'):
        os.makedirs('csv_scripts')

    df.to_csv(r'csv_scripts/sponsor_type.csv', index=False, header=False)

    create_table_query = '''CREATE TABLE ctgov.sponsor_type
                            (nct_id varchar(15), sponsor_category varchar(25));'''
    cursor.execute(create_table_query)
    connection.commit()

    f = open('csv_scripts/sponsor_type.csv')

    cursor.copy_from(f, 'ctgov.sponsor_type', columns=None, sep=",")
    print("Table populated successfully.")

    connection.commit()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Closing database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
