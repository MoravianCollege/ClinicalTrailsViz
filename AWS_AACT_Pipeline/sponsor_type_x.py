# coding=utf-8
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import re

# load information from .env file to log in and connect to the database
load_dotenv()
host = os.getenv('DBHost')
port = os.getenv('DBPort')
database_name = os.getenv('DBName')
user = os.getenv('MasterUsername')
password = os.getenv('password')

# connect to the database
connection = psycopg2.connect(
    database=database_name,
    user=user,
    password=password,
    host=host,
    port=port
)

# initiated variables to create the new column
sql_command = "SELECT nct_id, name FROM ctgov.sponsors"
new_column_name = 'sponsor_category'

# retrieve wanted data from the query (in the form of a data frame)
df = pd.read_sql_query(sql_command, con=connection)

# check conditions_list.txt to determine the value to be assigned for the row in the new column
df[new_column_name] = np.where(df.name.str.contains("college|school|univers|higher education|academy", flags=re.IGNORECASE,),"Education",
                         np.where(df.name.str.contains('hospital|hopit|hospice|hôpitaux', flags=re.IGNORECASE), "Hospitals",
                         np.where(df.name.str.contains('pharmac', flags=re.IGNORECASE), "Pharmaceuticals",
                         np.where(df.name.str.contains('research|laborator', flags=re.IGNORECASE), "Research Teams",
                         np.where(df.name.str.contains('institu|istituto', flags=re.IGNORECASE), 'Institutions',
                         np.where(df.name.str.contains('center|centre|centro|group|medicine|health|medical|clinic', flags=re.IGNORECASE), 'Medicine & Health',
                         np.where(df.name.str.contains('foundation|fund|fondation|fondazione', flags=re.IGNORECASE), "Foundations",
                         np.where(df.name.str.contains(' inc |inc\\.|co\\.|company|corpor|corp\\.|incorporated|ltd\\.|llc\\.|ltd| inc| llc', flags=re.IGNORECASE), 'Companies',
                         np.where(df.name.str.contains('united states|government', flags=re.IGNORECASE), 'Government',
                         "Other")))))))))

# will print the new categories and their counts for the created column
print(df[new_column_name].value_counts())

# will print the table from the sql command + the new column added
#print(df)
# print("--------------\n")

connection.close()

df.drop('name', axis=1, inplace=True)

df.to_csv(r'/Users/BAnderson/Merck-Summer-2019/ClinicalTrialsViz/AWS_AACT_Pipeline/csv_scripts/sponsor_type.csv')


try:
    # Get information to connect to database
    load_dotenv()
    username = os.getenv('username')
    password = os.getenv('password')
    hostname = os.getenv('hostname')
    database = os.getenv('database')
    port = os.getenv('port')

    # Connect to database
    connection = psycopg2.connect(
        user=username,
        password=password,
        host=hostname,
        database=database,
        port=port,
    )

    cursor = connection.cursor()

    column_name = "sponsor_type"

    # Create and execute column creation query
    create_new_column = '''ALTER TABLE ctgov.Transformed_Data 
              ADD COLUMN {} VARCHAR;'''.format(column_name)
    cursor.execute(create_new_column)
    connection.commit()
    print("New column successfully created \n")

    # Populate test column with 0s and 1s
    populate_column_true = '''UPDATE ctgov.Transformed_Data
              SET {} = '{}' WHERE ctgov.Transformed_Data.nct_id = '{}';'''.format(column_name, df.values[5], df.values[1])
    cursor.execute(populate_column_true)

    connection.commit()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Closing database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
