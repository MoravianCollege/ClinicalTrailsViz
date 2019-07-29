from AWS_AACT_Pipeline.categorizer import Categorizer
from AWS_AACT_Pipeline.database_manager import DatabaseManager


class Driver:

    def __init__(self, database_manager):

        self.database_manager = database_manager
        self.categorizer = Categorizer()

    def make_connection(self):
        self.database_manager.make_connection()

    def make_new_tables(self, original_table, original_col, new_table, new_column, json_key_file, extra_sql_command=''):
        print("\n")
        print("Starting categorization...")
        self.database_manager.delete_table_if_exists(new_table)
        print("Processing data...")

        if "extra_sql_command" is not '':
            self.database_manager.make_data_frame(original_col, original_table, extra_sql_command)
        else:
            self.database_manager.make_data_frame(original_col, original_table)

        self.categorizer.read_file_conditions(json_key_file)
        categorized_df = self.categorizer.categorize(original_col, new_column, self.database_manager.get_data_frame())
        self.database_manager.make_new_table(categorized_df, new_table, new_column)

    def close_connection(self):
        self.database_manager.close_connection()


if __name__ == '__main__':

    database_conn = DatabaseManager()
    driver = Driver(database_conn)

    try:
        driver.make_connection()
        print("Connection made successfully")

        # make new tables for each of our algorithms

        driver.make_new_tables(original_table="studies",
                               original_col="why_stopped",
                               new_table="why_stopped_table",
                               new_column="stop_reason",
                               json_key_file="why_stopped_key",
                               extra_sql_command=" WHERE why_stopped IS NOT NULL")

        driver.make_new_tables(original_table="sponsors",
                               original_col="name",
                               new_table="sponsor_type",
                               new_column="sponsor_category",
                               json_key_file="sponsors_key")

        driver.make_new_tables(original_table="sponsors",
                               original_col="name",
                               new_table="lead_sponsor_type",
                               new_column="sponsor",
                               json_key_file="sponsors_key",
                               extra_sql_command=" WHERE lead_or_collaborator = 'lead'")

        driver.make_new_tables(original_table="conditions",
                               original_col="downcase_name",
                               new_table="condition_type",
                               new_column="condition_category",
                               json_key_file="conditions_key")

    except Exception as error:
        print(error)

    finally:
        # Closing database connection
        driver.close_connection()
        print("Categorization complete\n")