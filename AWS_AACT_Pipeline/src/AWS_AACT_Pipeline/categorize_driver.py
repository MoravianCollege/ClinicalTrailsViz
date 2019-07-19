from AWS_AACT_Pipeline.ConditionCategorizer import ConditionCategorizer

# Categorizer entry format: (original_table, original_col, new_table, new_column, json_key_file)
driver = ConditionCategorizer('conditions', 'downcase_name', 'condition_type', 'condition_category', 'conditions_key')
driver2 = ConditionCategorizer('studies', 'why_stopped', 'why_stopped_table', 'stop_reason', 'why_stopped_key')

drivers = [driver, driver2]
print("Starting categorization...")

for driver in drivers:
    try:
        driver.make_connection()
        print("Connection made successfully")

        driver.delete_table_if_exists()
        driver.make_data_frame()
        driver.read_file_conditions()

        driver.categorize()
        print("Categorization complete")

        driver.make_new_table()

    except Exception as error:
        print(error)

    finally:
        # Closing database connection
        driver.close_connection()
