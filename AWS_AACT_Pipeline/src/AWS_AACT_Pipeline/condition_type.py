import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import sys
import json
import re

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

    # initiated variables to create the new column - fill as needed
    sql_command = "SELECT nct_id, downcase_name FROM ctgov.conditions"
    new_column_name = "condition_type"
    filename = "conditions_key"
    original_col = "downcase_name"
    nan_filler = "Other"

    # Delete table if it exists
    table_name = "condition_type"
    # Create and execute table deletion query
    delete_table_query = '''DROP TABLE IF EXISTS ctgov.{};'''.format(table_name)
    cursor.execute(delete_table_query)

    connection.commit()
    print("Table {} successfully deleted from PostgreSQL".format(table_name))

    # retrieve necessary data in the form of a data frame
    df = pd.read_sql_query(sql_command, con=connection)

    # function to open JSON file, read, and obtain/return the object with the file's information
    def read_file_conditions():
        with open(filename, 'r') as myfile:
            data = myfile.read()

        obj = json.loads(data)
        return obj

    # function checks conditions based on the values in the JSON file - used to apply to each row in the data frame
    def check_conditions(name):
        obj = read_file_conditions()
        result = nan_filler
        is_condition_met = False
        for label in obj:
            for comparison in obj[label]:
                if re.search(comparison, name) is not None:
                    result = label
                    is_condition_met = True
                    break
            if is_condition_met:
                break
        return result


    # retrieve and vectorize the function to be applied to each row in the data frame
    func = np.vectorize(check_conditions)

    # apply the function to the data frame
    condition_type = func(df[original_col])

    # adds the new column to the data frame with new column name
    df[new_column_name] = condition_type

    # prints the counts for each category in the new column (just so the user can see results)
    print(df[new_column_name].value_counts())

    df.drop(original_col, axis=1, inplace=True)

    create_table_query = '''CREATE TABLE ctgov.condition_type
                                (nct_id varchar(15), sponsor_category varchar(30));'''
    cursor.execute(create_table_query)
    connection.commit()

    # Create a directory for csv information if it doesn't exist yet
    if not os.path.exists('csv_scripts'):
        os.makedirs('csv_scripts')

    df.to_csv(r'csv_scripts/condition_type.csv', index=False, header=False)
    f = open('csv_scripts/condition_type.csv')

    cursor.copy_from(f, 'ctgov.condition_type', columns=None, sep=",")
    print("Table {} populated successfully".format(table_name))

    connection.commit()

except Exception as error:
    print(error)

finally:
    # Closing database connection
    if connection:
        cursor.close()
        connection.close()