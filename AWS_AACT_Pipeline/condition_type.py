# coding=utf-8
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import sys

try:
    # load information from .env file to log in and connect to the database
    load_dotenv()
    MasterUsername = os.getenv('MasterUsername')
    MasterUserPassword = os.getenv('MasterUserPassword')
    hostname = sys.argv[1]
    DBName = os.getenv('DBName')
    DBPort = os.getenv('DBPort')

    # Connect to database
    connection = psycopg2.connect(
        user=MasterUsername,
        password=MasterUserPassword,
        host=hostname,
        database=DBName,
        port=DBPort)

    cursor = connection.cursor()

    # initiated variables to create the new column
    sql_command = "SELECT nct_id, downcase_mesh_term FROM ctgov.browse_conditions"
    new_column_name = 'condition_type'

    # retrieve wanted data from the query (in the form of a data frame)
    df = pd.read_sql_query(sql_command, con=connection)

    # check conditions to determine the value to be assigned for the row in the new column
    col = 'downcase_mesh_term'
    conditions = [
        df[col].str.contains("cancer|lymphoma|leukemia|melanoma|carcinoma|neoplasm|mesothelioma|sarcoma|glioblastoma"),
        df[col].str.contains(
            "hiv|influen|immune deficiency|malaria|hepatitis|sepsis|tuberculosis|pneumonia|(?<![\w\d])infection(?![\w\d])",
            regex=True),
        df[col].str.contains("multiple sclerosis|parkinson|alzheim|dementia|epilepsy|brain|cognitive impair|migraine"),
        df[col].str.contains("healthy"),
        df[col].str.contains("obesity|diabete|metaboli|weight|thyroid|insulin|cholesterol|vitamin|nutrition"),
        df[col].str.contains("cardio|heart|atria|arter|coronar|atherosclerosis"),
        df[col].str.contains("asthma|pulmonary disease|respirator|copd|sleep apnea|smok"),
        df[col].str.contains("anxi|depress|schizo|bipolar|psychosis|autism|insomnia"),
        df[col].str.contains("stroke"),
        df[col].str.contains("rheuma|inflamma"),
        df[col].str.contains("osteoarthritis|osteoporosis|fibromyalgia"),
        df[col].str.contains(
            "pregn|infertil|birth|contracept|abortion|mammary|menstruat|menopause|in vitro|(?<![\w\d])art(?![\w\d])",
            regex=True),
        df[col].str.contains("cystic fibrosis|cerebral"),
        df[col].str.contains("anemi|myelodysplastic|sickle"),
        df[col].str.contains("kidney|(?<![\w\d])renal(?![\w\d])", regex=True),
        df[col].str.contains("psoriasis|dermat"),
        df[col].str.contains("glaucoma|cataract|myopia|oculur"),
        df[col].str.contains("crohn|bowel|colitis")]

    choices = ["Oncology", "Infection", "Neurology", "Healthy", "Metabolic & Endocrine", "Cardiovascular",
               "Respiratory",
               "Mental Health", "Stroke", "Inflammatory & Immune", "Musculoskeletal", "Reproductive",
               "Congenital Disorders",
               "Blood", "Renal & Urogenital", "Skin", "Eye", "Oral & Gastrointestinal"]

    df["condition_type"] = np.select(conditions, choices, "Other")

    df.drop('downcase_mesh_term', axis=1, inplace=True)

    create_table_query = '''CREATE TABLE ctgov.condition_type
                                (nct_id varchar(15), sponsor_category varchar(30));'''
    cursor.execute(create_table_query)
    connection.commit()

    # Create a directory for csv information if it doesn't exist yet
    if not os.path.exists('csv_scripts'):
        os.makedirs('csv_scripts')

    df.to_csv(r'csv_scripts/condition_type.csv', index=False, header=False)
    f = open('csv_scripts/condition_type.csv')

    cursor.copy_from(f, 'ctgov.condition_type', columns=None, sep=",")
    print("Table populated successfully.")

    connection.commit()
    connection.close()

except Exception as error:
    print(error)
