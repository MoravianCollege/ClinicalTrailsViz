# Explanation on condition_type.py

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

## How We Categorize Condition Type

### The JSON File
* The JSON file ```condition_keys``` contains keys or labels associated with keywords
  * For example, the *Oncology* label's first keyword is *cancer*, because if the condition name contains the word *cancer*, it should be placed in the *Oncology* category.
* Keywords can easily be added to categories and new categories can be added as needed as long as you follow the same JSON format
* Note that in some cases regular expressions may make checks easier
  * For example, the only regular expression pattern currently used in the file looks similar to this: ```(?<![\w\d])art(?![\w\d])```
  * Although it seems complicated, this allows for a search in a string that contains the specific word *art*, and will not pick up patterns such as *artery* or *heart*.

### Calculating the category
1. Initiated variables:
  * ```sql_command``` : the command you wish to query in order to retrieve tables, columns, etc. from the database, i.e. ```"SELECT nct_id, downcase_name FROM ctgov.conditions"```
  * ```new_column_name``` : the name of the new column you wish to create, i.e. ```"condition_type"```
  * ```filename``` : the name of the JSON file containing the pairs, i.e. ```condition_keys```
  * ```original_col``` : the name of the original column to use in comparisons, determining the outcome for the new column, i.e. ```"downcase_name"```
  * ```"nan_filler"``` : the name of the category you wish to place all of the values that do not apply to your new categories, i.e. ```"Other"```
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

## Further Use
This pattern can be followed for any other variables you wish to categorize. To experiment with other variables, create a JSON file containing the categories as labels and list the keywords you wish to be used to associate with those labels. Then, change the five *initiated varibles* to the values you need or prefer. 
