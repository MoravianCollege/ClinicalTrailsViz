import os
import psycopg2
from dotenv import load_dotenv


try:
    # Get information to connect to database
    load_dotenv()
    username = os.getenv('username')
    password = os.getenv('password')
    hostname = os.getenv('hostname')
    database = os.getenv('database')
    port = os.getenv('port')

    # Connect to database
    connection = psycopg2.connect(
        user=username,
        password=password,
        host=hostname,
        database=database,
        port=port
    )
    cursor = connection.cursor()

    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to:", record, "\n")

    # Create and execute table creation query
    create_table_query = '''CREATE TABLE Transformed_Data AS
              SELECT nct_id FROM ctgov.Studies;'''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table successfully created in PostgreSQL \n")

    # Set nct_id as primary key
    set_primary_key = '''ALTER TABLE Transformed_Data 
              ADD PRIMARY KEY (nct_id);'''
    cursor.execute(set_primary_key)
    connection.commit()
    print("Primary key successfully set \n")

    # Create and execute column creation query
    create_new_column = '''ALTER TABLE Transformed_Data 
              ADD COLUMN test_var INTEGER;'''
    cursor.execute(create_new_column)
    connection.commit()
    print("New column successfully created \n")

    # Populate test column with boolean values
    populate_column_true = '''UPDATE Transformed_Data
              SET test_var = mod(cast(substr(nct_id, 4, 8) AS INTEGER), 2);'''
    cursor.execute(populate_column_true)
    connection.commit()
    print("New column successfully populated \n")
    converted_column = '''ALTER TABLE Transformed_Data 
              ALTER COLUMN test_var 
              TYPE integer 
              USING (test_var::integer);'''
    cursor.execute(converted_column)
    connection.commit()
    print("Column type has been converted \n")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Closing database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
