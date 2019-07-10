# coding=utf-8
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import numpy as np
import re

# load information from .venv file to log in and connect to the database
load_dotenv()
host = os.getenv('hostname')
port = os.getenv('port')
database_name = os.getenv('database')
user = os.getenv('username')
password = os.getenv('password')

# connect to the database
connection = psycopg2.connect(
    database=database_name,
    user=user,
    password=password,
    host=host,
    port=port
)

# initiated variables to create the new column
sql_command = "SELECT * FROM ctgov.conditions"
new_column_name = 'condition_type'

# retrieve wanted data from the query (in the form of a data frame)
df = pd.read_sql_query(sql_command, con=connection)

# check conditions to determine the value to be assigned for the row in the new column
col = 'downcase_name'
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

choices = ["Oncology", "Infection", "Neurology", "Healthy", "Metabolic & Endocrine", "Cardiovascular", "Respiratory",
           "Mental Health", "Stroke", "Inflammatory & Immune", "Musculoskeletal", "Reproductive",
           "Congenital Disorders",
           "Blood", "Renal & Urogenital", "Skin", "Eye", "Oral & Gastrointestinal"]

df["condition_type"] = np.select(conditions, choices, "Other")

# will print the new categories and their counts for the created column
print(df[new_column_name].value_counts())

# will print the table from the sql command + the new column added
print(df)

connection.close()
