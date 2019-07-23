import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import sys
import json
import re


class Categorizer(object):

    def __init__(self, original_table, original_col, new_table_name,
                 new_column_name, json_key_file, extra_sql_query=""):
        # load information from .env file to log in and connect to the database
        load_dotenv()
        self.MasterUsername = os.getenv('MasterUsername')
        self.MasterUserPassword = os.getenv('MasterUserPassword')
        self.hostname = sys.argv[1]
        self.DBName = os.getenv('DBName')
        self.DBPort = os.getenv('DBPort')

        # other initiated variables to be changed when categorizing
        self.connection = None
        self.df = None
        self.obj = None

        # customizable variables: can change if doing a different categorization

        self.original_table = original_table
        self.original_col = original_col
        self.new_table_name = new_table_name
        self.new_column_name = new_column_name
        self.filename = json_key_file
        self.extra_sql_query = extra_sql_query

        self.nan_filler = "Other"
        self.sql_command = "SELECT nct_id, {} FROM ctgov.{} {}".format(self.original_col, self.original_table, self.extra_sql_query)

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
        # Create and execute table deletion query
        delete_table_query = '''DROP TABLE IF EXISTS ctgov.{};'''.format(self.new_table_name)
        self.get_cursor().execute(delete_table_query)

        self.connection.commit()
        print("Table {} successfully deleted from PostgreSQL".format(self.new_table_name))

    def read_file_conditions(self):
        # Get file location
        file_path = os.path.dirname(os.path.abspath(__file__))
        parent = os.path.dirname(os.path.dirname(file_path))
        data_path = os.path.join(parent, "json_keys/" + self.filename)

        with open(data_path, 'r') as file:
            data = file.read()
        self.obj = json.loads(data)

    def make_data_frame(self):
        self.df = pd.read_sql_query(self.sql_command, con=self.connection)
        # Set all column values to lower case
        self.df['{}'.format(self.original_col)] = self.df['{}'.format(self.original_col)].str.lower()

    def check_conditions(self, name):
        result = self.nan_filler
        is_condition_met = False
        for label in self.obj:
            for comparison in self.obj[label]:
                if re.search(comparison, str(name)) is not None:
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
        create_table_query = '''CREATE TABLE ctgov.{}
                                            (nct_id varchar(15), {} varchar(30));''' \
            .format(self.new_table_name, self.new_column_name)
        self.get_cursor().execute(create_table_query)
        self.connection.commit()
        # Create a directory for csv information if it doesn't exist yet
        if not os.path.exists('csv_scripts'):
            os.makedirs('csv_scripts')

        self.df.to_csv(r'csv_scripts/{}.csv'.format(self.new_table_name), index=False, header=False)
        f = open('csv_scripts/{}.csv'.format(self.new_table_name))

        self.get_cursor().copy_from(f, 'ctgov.{}'.format(self.new_table_name), columns=None, sep=",")
        print("Table {} populated successfully".format(self.new_table_name))

        self.connection.commit()

    def close_connection(self):
        # Closing database connection
        if self.connection:
            self.get_cursor().close()
            self.connection.close()
