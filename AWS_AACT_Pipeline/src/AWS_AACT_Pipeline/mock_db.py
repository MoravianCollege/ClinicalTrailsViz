

class MockDatabase:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def make_connection(self):
        pass

    def delete_table_if_exists(self, table):
        pass

    def make_data_frame(self, original_col, original_table, extra_sql_query=''):
        pass