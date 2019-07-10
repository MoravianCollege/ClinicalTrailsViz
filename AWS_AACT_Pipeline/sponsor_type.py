# coding=utf-8
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import re

# load information from .venv file to log in and connect to the database
load_dotenv()
host = os.getenv('hostname')
port = os.getenv('port')
database_name = os.getenv('database')
user = os.getenv('username')
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
sql_command = "SELECT * FROM ctgov.sponsors"
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
print(df)

connection.close()