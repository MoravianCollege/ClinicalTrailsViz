from AWS_AACT_Pipeline.Categorizer import Categorizer
from AWS_AACT_Pipeline.database_manager import DatabaseManager

# Categorizer entry format: (original_table, original_col, new_table, new_column, json_key_file)
#driver = Categorizer('conditions', 'downcase_name', 'condition_type', 'condition_category', 'conditions_key')
#driver2 = Categorizer('studies', 'why_stopped', 'why_stopped_table', 'stop_reason', 'why_stopped_key')
database_manager = DatabaseManager()
categorizer = Categorizer(database_manager)
#driver3 = Categorizer('sponsors', 'name', 'sponsor_type', 'sponsor_category', 'sponsors_key')
#driver4 = Categorizer('sponsors', 'name', 'lead_sponsor_type', 'sponsor',
                      #'sponsors_key', "where lead_or_collaborator = 'lead'")

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
    "extra_sql_command": "where lead_or_collaborator = 'lead'"
}

list_of_tables = [conditions, why_stopped, all_sponsors, lead_sponsors]

print("Starting categorization...")

for table in list_of_tables:
    try:
        database_manager.make_connection()
        print("Connection made successfully")
    
        database_manager.delete_table_if_exists(table["new_table"])
        print("Processing data...")
        database_manager.make_data_frame(table["original_col"], table["original_table"])  # need to add extra sql query if necessary
        categorizer.read_file_conditions(table["json_key_file"])
    
        categorizer.categorize(table['original_col'], table['new_column'])
        database_manager.make_new_table(table['original_col'], table["new_table"], table["new_column"])

    except Exception as error:
        print(error)

    finally:
        # Closing database connection
        database_manager.close_connection()
        print("Categorization complete\n")


'''for driver in drivers:
    try:
        database_manager.make_connection()
        print("Connection made successfully")

        database_manager.delete_table_if_exists("sponsor_type")
        print("Processing data...")
        database_manager.make_data_frame("name", "sponsors") # need to add extra sql query if necessary
        driver.read_file_conditions("sponsors_key")

        driver.categorize('name', 'sponsor_category')
        database_manager.make_new_table("name", "sponsor_type", "sponsor_category")

    except Exception as error:
        print(error)

    finally:
        # Closing database connection
        database_manager.close_connection()
        print("Categorization complete\n")'''
