from AWS_AACT_Pipeline.Categorizer import Categorizer
from AWS_AACT_Pipeline.database_manager import DatabaseManager

database_manager = DatabaseManager()
categorizer = Categorizer()

conditions = {
    "original_table": 'conditions',
    "original_col": 'downcase_name',
    "new_table": 'condition_type',
    "new_column": 'condition_category',
    "json_key_file": 'conditions_key'
}

why_stopped = {
    "original_table": 'studies',
    "original_col": 'why_stopped',
    "new_table": 'why_stopped_table',
    "new_column": 'stop_reason',
    "json_key_file": 'why_stopped_key'
}

all_sponsors = {
    "original_table": 'sponsors',
    "original_col": 'name',
    "new_table": 'sponsor_type',
    "new_column": 'sponsor_category',
    "json_key_file": 'sponsors_key'
}

lead_sponsors =  {
    "original_table": 'sponsors',
    "original_col": 'name',
    "new_table": 'lead_sponsor_type',
    "new_column": 'sponsor',
    "json_key_file": 'sponsors_key',
    "extra_sql_command": " WHERE lead_or_collaborator = 'lead'"
}

list_of_tables = [all_sponsors, lead_sponsors]

print("Starting categorization...")

for table in list_of_tables:
    try:
        database_manager.make_connection()
        print("Connection made successfully")
    
        database_manager.delete_table_if_exists(table["new_table"])
        print("Processing data...")

        if "extra_sql_command" in table:
            database_manager.make_data_frame(table["original_col"],
                                             table["original_table"],
                                             table["extra_sql_command"])
        else:
            database_manager.make_data_frame(table["original_col"],
                                             table["original_table"])

        categorizer.read_file_conditions(table["json_key_file"])
    
        categorizer.categorize(table['original_col'], table['new_column'], database_manager.get_data_frame())
        database_manager.make_new_table(table['original_col'], table["new_table"], table["new_column"])

    except Exception as error:
        print(error)

    finally:
        # Closing database connection
        database_manager.close_connection()
        print("Categorization complete\n")
