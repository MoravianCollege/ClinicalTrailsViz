from AWS_AACT_Pipeline.condition_type import ConditionCategorizer

driver = ConditionCategorizer()

print("Starting categorization...")

try:
    driver.make_connection()
    print("Connection made successfully")

    driver.delete_table_if_exists()
    driver.make_data_frame()
    driver.read_file_conditions()

    driver.categorize()
    print("Categorization complete")

    driver.make_new_table()
    print(driver.table_name, "was created successfully")

except Exception as error:
    print(error)

finally:
    # Closing database connection
    driver.close_connection()
