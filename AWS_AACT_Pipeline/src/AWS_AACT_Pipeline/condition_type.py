import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import sys
import json
import re


class ConditionCategorizer:

    def __init__(self):
        # load information from .env file to log in and connect to the database
        load_dotenv()
        self.MasterUsername = os.getenv('MasterUsername')
        self.MasterUserPassword = os.getenv('MasterUserPassword')
        self.hostname = 'clinicaltrialsdatabase.cfdgyctoflg4.us-east-2.rds.amazonaws.com'
        self.DBName = "aact"
        self.DBPort = os.getenv('DBPort')

        # other initiated variables to be changed when categorizing
        self.connection = None
        self.df = None
        self.obj = None

        # customizable variables: can change if doing a different categorization
        self.sql_command = "SELECT nct_id, downcase_name FROM ctgov.conditions"
        self.new_column_name = "condition_type"
        self.filename = "/Users/kylienorwood/ComputerScience/MerckSummer19/ClinicalTrialsViz/AWS_AACT_Pipeline/conditions_key"
        self.original_col = "downcase_name"
        self.nan_filler = "Other"
        self.table_name = "condition_type"

    def make_connection(self):
        # Connect to database
        self.connection = psycopg2.connect(
            user=self.MasterUsername,
            password=self.MasterUserPassword,
            host=self.hostname,
            database=self.DBName,
            port=self.DBPort)

    def get_cursor(self):
        cursor = self.connection.cursor()
        return cursor

    def delete_table_if_exists(self):
        # Delete table if it exists
        table_name = "condition_type"
        # Create and execute table deletion query
        delete_table_query = '''DROP TABLE IF EXISTS ctgov.{};'''.format(table_name)
        self.get_cursor().execute(delete_table_query)

        self.connection.commit()
        print("Table {} successfully deleted from PostgreSQL".format(table_name))

    def read_file_conditions(self):
        with open(self.filename, 'r') as myfile:
            data = myfile.read()
        self.obj = json.loads(data)

    def make_data_frame(self):
        self.df = pd.read_sql_query(self.sql_command, con=self.connection)

    def check_conditions(self, name):
        result = self.nan_filler
        is_condition_met = False
        for label in self.obj:
            for comparison in self.obj[label]:
                if re.search(comparison, name) is not None:
                    result = label
                    is_condition_met = True
                    break
            if is_condition_met:
                break
        return result

    def categorize(self):
        func = np.vectorize(self.check_conditions)
        condition_type = func(self.df[self.original_col])
        self.df[self.new_column_name] = condition_type

        # print value counts so the user can see the categorization numbers for the new column
        print("Value counts for " + self.new_column_name + ": ")
        print(self.df[self.new_column_name].value_counts())

    def make_new_table(self):
        self.df.drop(self.original_col, axis=1, inplace=True)
        create_table_query = '''CREATE TABLE ctgov.condition_type
                                            (nct_id varchar(15), sponsor_category varchar(30));'''
        self.get_cursor().execute(create_table_query)
        self.connection.commit()
        # Create a directory for csv information if it doesn't exist yet
        if not os.path.exists('csv_scripts'):
            os.makedirs('csv_scripts')

        self.df.to_csv(r'csv_scripts/condition_type.csv', index=False, header=False)
        f = open('csv_scripts/condition_type.csv')

        self.get_cursor().copy_from(f, 'ctgov.condition_type', columns=None, sep=",")
        print("Table {} populated successfully".format(self.table_name))

        self.connection.commit()

    def close_connection(self):
        # Closing database connection
        if self.connection:
            self.get_cursor().close()
            self.connection.close()
