from AWS_AACT_Pipeline.Categorizer import Categorizer

# Categorizer entry format: (original_table, original_col, new_table, new_column, json_key_file)
driver = Categorizer('conditions', 'downcase_name', 'condition_type', 'condition_category', 'conditions_key')
driver2 = Categorizer('studies', 'why_stopped', 'why_stopped_table', 'stop_reason', 'why_stopped_key')
driver3 = Categorizer('sponsors', 'name', 'sponsor_type', 'sponsor_category', 'sponsors_key')

drivers = [driver, driver2, driver3]
print("Starting categorization...")

for driver in drivers:
    try:
        driver.make_connection()
        print("Connection made successfully")

        driver.delete_table_if_exists()
        print("Processing data...")
        driver.make_data_frame()
        driver.read_file_conditions()

        driver.categorize()
        driver.make_new_table()

    except Exception as error:
        print(error)

    finally:
        # Closing database connection
        driver.close_connection()
        print("Categorization complete\n")
