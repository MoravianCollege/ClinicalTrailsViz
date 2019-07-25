

class MockDatabaseManager:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def make_connection(self):
        pass

    def delete_table_if_exists(self, table):
        pass

    def make_data_frame(self, original_col, original_table, extra_sql_query=''):
        pass

    def get_data_frame(self):
        return self.dataframe

    def make_new_table(self, dataframe, new_table, new_column):
        self.final_dataframe = dataframe

    def close_connection(self):
        pass

    def get_final_dataframe(self):
        return self.final_dataframe
