# Explanation on categorizer.py

## Background
### The Database
* We currently have our own AWS RDS instance of the AACT Database available
* As a result, we can add or delete columns, tables, etc. as we please
* About 40% of variables in the database are free-text and descriptive, making it difficult to produce any visualizations for those variables



As a result, we have decided to develop a program that will sort variables into new categorical variables, assisting us in utilizing these useful descriptive variables. Below explains how we categorize these variables - we use condition type as an example to help clarify.

## How We Categorize Variables Such As Condition Type

### The JSON File
* The JSON file resides in the ```json_keys``` directory under the ```AWS_AACT_Pipeline``` directory. The files (in this case ```condition_keys```) contain keys/labels associated with keywords that help determine which category an entry will be placed in.
  * For example, the *Oncology* label's first keyword is *cancer*, because if the condition name contains the word *cancer*, it should be placed in the *Oncology* category.
* Keywords can easily be added or deleted to and from categories and new categories can be added as needed as long as you follow the same JSON format
* Note that in some cases regular expressions may make checks easier
  * For example, the only regular expression pattern currently used in the file looks similar to this: ```(?<![\w\d])art(?![\w\d])```
  * Although it seems complicated, this allows for a search in a string that contains the specific word *art*, and will not pick up patterns such as *artery* or *heart*.

### Calculating the category

#### categorize_driver.py
The Driver class performs all calculations (calls all necessary methods from the other classes). The class takes a DatabaseManager as a parameter (so that we only have one connection happening). When initialized, we create a new categorizer and the DatabaseManager parameter is set.

1. ```make_connection```: calls the make connection function from the DatabaseManager
2. ```make_new_tables(original_table, original_col, new_table, new_column, json_key_file, extra_sql_query='')```: this is the main function. It calls methods from both the DatabaseManager and the Categorizer. In this order: ```delete_table_if_exists```, ```make_data_frame```, ```read_file_conditions```, ```categorize```, ```make_new_table```.
3. ```close_connection```: calls the close connection function from the DatabaseManager

Explantion on the variables passed to ```make_new_tables```:

* ```original_table```: the name of the original table from the AACT Database to use in comparisons, i.e. ```conditions```
* ```original_col``` : the name of the original column to use in comparisons, determining the outcome for the new column, i.e. ```downcase_name```
* ```new_table``` : the name of the new table you wish to create, i.e. ```condition_type```
* ```new_column``` : the name of the new column you wish to create, i.e. ```condition_category```
* ```json_key_file```: the name of the JSON file containing the pairs, i.e. ```condition_keys```
* ```extra_sql_command=''```: contains an extra query if needed, i.e. ```"WHERE downcase_name='parkinson'"```

The bottom of this file contains a ```main``` (separate from the Driver class) that creates a new DatabaseManager and a new Driver, taking that DatabaseManager as a parameter. It then tries to make a connection, calls ```make_new_tables``` on each table we wish to create, and will then close the connection.

#### categorizer.py
The Categorizer class handles all necessary calculations to perform the categorization of a variable.

1. ```read_file_conditions(filename)```: gets the location of the json file to be used to categorize, reads the file, and places results in an object containing the json's information - will throw an exception if json file cannot be found or if the file is misformatted
2. ```check_conditions(row)```: a method that reads the labels and keywords from the JSON file, compares those keywords to the value of the original column in a row
3. ```categorize(original_col, new_column_name, df)```: vectorizes the function, allowing execution on all of the rows simultaneously, instead of one by one (function is applied to the entire data frame at once). Once the new data frame is constructed, the ```original_col``` variable is dropped so the only remaining columns are ```nct_id``` and ```new_column_name```. Then, the program will print the value counts for each category in the new data frame, and returns the new, categorized data frame.

#### database_manager.py
The DatabaseManager class handles the necessary calculations that interact directly with the database.

When initialized, the class retrieves information in order to connect to the database (username, password, hostname, etc.).
1. ```make_connection()```: makes the connection to the database
2. ```get_cursor()```: gets the cursor that assists in making PostgreSQL commands
3. ```delete_table_if_exists(new_table_name)```: deletes the table from the database if it exists (in order to avoid duplication when making a new table)
4. ```make_data_frame(original_col, original_table, extra_sql_query='')```: queries the database to retrieve a data frame with nct_id and the column we wish to categorize
5. ```get_data_frame()```: getter to retrieve the current data frame
6. ```make_new_table(categorized_df, new_table_name, new_column_name)```: creates the new table and places it in the database - a table with the nct_id and the new column with its categorized values
  *  The categorized_df is sent to a csv file inside the ```csv_scripts``` directory. The ```boto3``` library then uses ```get_cursor().copy_from(file, new_table_name)``` and copies all data from the specified csv file into a new table in the database. This method was chosen as it proved to be the fastest to populate tables using bulk data insertion.
7. ```close_connection()```: closes the current cursor and connection to the database


## Further Use
This pattern can be followed for any other variables you wish to categorize. To experiment with other variables, create a JSON file containing the categories as labels and list the keywords you wish to be used to associate with those labels and place it in the directory labeled ```json_keys```. See the other json files within that directory to understand the formatting. Then, change the five *initiated varibles* to the values you need or prefer in the ```categorize_driver.py``` file.

## Variables we have categorized so far...

### Reason for Stopped trials
* In order to improve clinical trials, many are interested in studying why trials have been stopped
* About 16,000 distinct descriptions have been entered into the database (all free-text and descriptive)
* Categorizing this variable would help others determine the general reason clinical trials have been stopped, without having to read the descriptions
* List of categories: enrollment, accrual, lack of funding, logistic reasons, ineffective or futile, administrative decision, sponsor of PI decision, business decision, toxicity, feasibility reasons, safety, other.

### All Sponsor Types
* About 56,000 distinct sponsors have been entered into the database
* This variable includes ALL sponsors - meaning, leads and collaborators
* Categorizing sponsor names helps identify the types people/organizations that sponsor clinical trials (more general)
* List of categories: education, hospitals, government, pharmaceuticals, research & institutes, medicine and health groups, foundations, companies, other.

### Lead Sponsor Types
* Category essentially the same as above, but only categorizes the LEAD sponsor of a clinical trial
* List of categories the same as variable above.

### Condition Types
* One of the important variables for clinical trials: primary condition being
studied
* About 78,000 distinct condition types are studied in the trials within the database
* The goal of categorizing this variable would be to generalize these conditions in terms of therapeutic area, rather than a specific condition name
* Categories were determined based on the UK Clinical Research Collaboration's classifications, found [here](https://hrcsonline.net/health-categories/).
