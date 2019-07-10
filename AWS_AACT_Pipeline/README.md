#Setup


##Install AWS CLI
Install the AWS CLI with documentation [here] (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).


##Configure AWS CLI 
Configure the AWS CLI with your own amazon credentials. Documentation [here] (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).


##System evironment variables
1. Create a virtual environment named .venv `python3 -m venv .venv`

2. Activate the virtual environment `source .venv/bin/activate`

3. Install required libraries `pip install -r requirements.txt`

4. Install source of this repo as an editable package `pip install -e .`

5. Create the file .env containing our AWS database information (This file is listed in .gitignore because it should never go in the repo)

```
DBName=your_database_name
DBInstanceIdentifier=your_database_identifier
MasterUsername=your_username
MasterUserPassword=your_password
```


##Startup
Now that AWS CLI is configured and environment variables are created, run AWS\_Database\_Start.py to start your AWS RDS instance from scratch. 

**Disclaimer:**

* Database data takes approximately **7 minutes** to download depending on the internet connection.
* Populating the database takes approximately **35 minutes** with this instance configuration.
* AWS database instance size default is set to 20 gigabytes, the database as of July 8th, 2019 takes up about **10.5 gigabytes** of space after loaded onto the instance.