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

    # Create and execute table deletion query
    delete_table_query = '''DROP TABLE Transformed_Data;'''
    cursor.execute(delete_table_query)
    connection.commit()
    print("Table successfully deleted from PostgreSQL \n")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Closing database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
