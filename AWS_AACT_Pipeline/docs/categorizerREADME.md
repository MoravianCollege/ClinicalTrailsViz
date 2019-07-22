# Explanation on categorizer.py

## Background
### The Database
* We currently have our own AWS RDS instance of the AACT Database available
* As a result, we can add or delete columns, tables, etc. as we please
* About 40% of variables in the database are free-text and descriptive, making it difficult to produce any visualizations for those variables

### Condition Types
* One of the important variables for clinical trials: primary condition being
studied
* About 78,000 distinct condition types are studied in the trials within the database
* The goal of categorizing this variable would be to generalize these conditions in terms of therapeutic area, rather than a specific condition name
* Categories were determined based on the UK Clinical Research Collaboration's classifications, found [here](https://hrcsonline.net/health-categories/).

## How We Categorize Variables Such As Condition Type

### The JSON File
* The JSON file ```json_keys/condition_keys``` contains keys or labels associated with keywords
  * For example, the *Oncology* label's first keyword is *cancer*, because if the condition name contains the word *cancer*, it should be placed in the *Oncology* category.
* Keywords can easily be added to categories and new categories can be added as needed as long as you follow the same JSON format
* Note that in some cases regular expressions may make checks easier
  * For example, the only regular expression pattern currently used in the file looks similar to this: ```(?<![\w\d])art(?![\w\d])```
  * Although it seems complicated, this allows for a search in a string that contains the specific word *art*, and will not pick up patterns such as *artery* or *heart*.

### Calculating the category
1. Initiated variables:
  * ```new_table_name``` : the name of the new table you wish to create, i.e. ```condition_type```
  * ```new_column_name``` : the name of the new column you wish to create, i.e. ```condition_category```
  * ```filename``` : the name of the JSON file containing the pairs, i.e. ```condition_keys```
  * ```original_table```: the name of the original table to use in comparisons, i.e. ```conditions```
  * ```original_col``` : the name of the original column to use in comparisons, determining the outcome for the new column, i.e. ```downcase_name```
  * ```"nan_filler"``` : the name of the category you wish to place all of the values that do not apply to your new categories, i.e. ```"Other"```
  * ```sql_command``` : the command you wish to query in order to retrieve tables, columns, etc. from the database, this command will utilize the values entered for original_col and original_table to change which variable is to be categorized i.e. ```"SELECT nct_id, original_col FROM ctgov.original_table"```
2. Querying the database:
  * ```df = pd.read_sql_query(sql_command, con=connection)``` : retrieves the needed portion from the database as a Pandas data frame
3. Obtaining information from the file:
  * ```read_file_conditions()``` : reads the JSON file and obtains/returns the object containing the file's information
4. Function to check conditions:
  * ```check_conditions(name)``` : a method that reads the labels and keywords from the JSON file, compares those keywords to the value of ```original_col``` in a row
  * Used to apply to each row of the data frame
5. Vectorize the function:
  * ```func = np.vectorize(practice)``` : allows execution on all of the rows simultaneously, instead of one by one
  * Allows computation to perform much faster
6. Apply to the data frame:
  * ```condition_type = func(df[original_col])``` : applies the vectorized version of our function to the data frame, using the rows' values from ```original_col```
7. Add new column:
  * ```df[new_column_name] = condition_type``` : adds the new column to the data frame
8. Pushing data to database:
  * Once the new dataframe is constructed, the ```original_col``` variable is dropped so the only remaining columns are ```nct_id``` and ```new_column_name```, this data frame is then sent to a csv file inside the ```csv_scripts``` directory. The ```boto3``` library then uses ```get_cursor().copy_from(file, new_table_name)``` and copies all data from the specified csv file into a new table in the database. This method was chosen as it proved to be the fastest to populate tables using bulk data insertion.

## Further Use
This pattern can be followed for any other variables you wish to categorize. To experiment with other variables, create a JSON file containing the categories as labels and list the keywords you wish to be used to associate with those labels and place it in the folder labeled ```json_keys```. Then, change the five *initiated varibles* to the values you need or prefer in the ```categorize_driver.py``` file. 
