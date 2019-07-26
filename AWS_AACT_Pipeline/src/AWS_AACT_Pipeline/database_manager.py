import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import sys


class DatabaseManager(object):

    def __init__(self):
        # load information from .env file to log in and connect to the database
        load_dotenv()
        self.MasterUsername = os.getenv('MasterUsername')
        self.MasterUserPassword = os.getenv('MasterUserPassword')
        self.hostname = sys.argv[1]
        self.DBName = os.getenv('DBName')
        self.DBPort = os.getenv('DBPort')

        # connection variables changed later during data manipulation
        self.connection = None
        self.df = None

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

    def delete_table_if_exists(self, new_table_name):
        # Create and execute table deletion query
        delete_table_query = '''DROP TABLE IF EXISTS ctgov.{};'''.format(new_table_name)
        self.get_cursor().execute(delete_table_query)

        self.connection.commit()
        print("Table {} successfully deleted from PostgreSQL".format(new_table_name))

    def make_data_frame(self, original_col, original_table, extra_sql_command=''):
        sql_command = "SELECT nct_id, {} FROM ctgov.{}".format(original_col, original_table + extra_sql_command)
        self.df = pd.read_sql_query(sql_command, con=self.connection)

        # Set all column values to lower case
        self.df['{}'.format(original_col)] = self.df['{}'.format(original_col)].str.lower()

    def get_data_frame(self):
        return self.df

    def make_new_table(self, categorized_df, new_table_name, new_column_name):
        create_table_query = '''CREATE TABLE ctgov.{}
                                            (nct_id varchar(15), {} varchar(30));''' \
            .format(new_table_name, new_column_name)
        self.get_cursor().execute(create_table_query)
        self.connection.commit()
        # Create a directory for csv information if it doesn't exist yet
        if not os.path.exists('csv_scripts'):
            os.makedirs('csv_scripts')

        categorized_df.to_csv(r'csv_scripts/{}.csv'.format(new_table_name), index=False, header=False)
        f = open('csv_scripts/{}.csv'.format(new_table_name))

        self.get_cursor().copy_from(f, 'ctgov.{}'.format(new_table_name), columns=None, sep=",")
        print("Table {} populated successfully".format(new_table_name))

        self.connection.commit()

    def close_connection(self):
        # Closing database connection
        if self.connection:
            self.get_cursor().close()
            self.connection.close()
