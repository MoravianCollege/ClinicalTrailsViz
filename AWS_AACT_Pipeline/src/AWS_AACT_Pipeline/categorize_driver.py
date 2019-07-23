from AWS_AACT_Pipeline.Categorizer import Categorizer
from AWS_AACT_Pipeline.database_manager import DatabaseManager

# Categorizer entry format: (original_table, original_col, new_table, new_column, json_key_file)
#driver = Categorizer('conditions', 'downcase_name', 'condition_type', 'condition_category', 'conditions_key')
#driver2 = Categorizer('studies', 'why_stopped', 'why_stopped_table', 'stop_reason', 'why_stopped_key')
database_manager = DatabaseManager()
driver1 = Categorizer(database_manager)
driver2 = Categorizer(database_manager)
driver3 = Categorizer(database_manager)
driver4 = Categorizer(database_manager)
#driver3 = Categorizer('sponsors', 'name', 'sponsor_type', 'sponsor_category', 'sponsors_key')
#driver4 = Categorizer('sponsors', 'name', 'lead_sponsor_type', 'sponsor',
                      #'sponsors_key', "where lead_or_collaborator = 'lead'")



drivers = [driver3]
print("Starting categorization...")

for driver in drivers:
    try:
        database_manager.make_connection()
        print("Connection made successfully")

        database_manager.delete_table_if_exists("sponsor_type")
        print("Processing data...")
        database_manager.make_data_frame("name", "sponsors")
        driver.read_file_conditions("sponsors_key")

        driver.categorize('name', 'sponsor_category')
        database_manager.make_new_table("name", "sponsor_type", "sponsor_category")

    except Exception as error:
        print(error)

    finally:
        # Closing database connection
        database_manager.close_connection()
        print("Categorization complete\n")
