# Setup


## Install AWS CLI
Install the AWS CLI with documentation [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).


## Configure AWS CLI 
Configure the AWS CLI with your own amazon credentials. Documentation [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).


## System evironment variables
1. Create a virtual environment named .venv `python3 -m venv .venv`

2. Activate the virtual environment `source .venv/bin/activate`

3. Install required libraries `pip install -r requirements.txt`

4. Install source of this repo as an editable package `pip install -e .`

5. Create the file .env containing our AWS database information (This file should be listed in .gitignore as it should never go in the repo)

```
DBPort=5432
Temp_DBName=your_database_name
DBName=aact_back
DBInstanceIdentifier=your_database_identifier
MasterUsername=your_username
MasterUserPassword=your_password
```

'aact_back' is the name of the database that the aact .dmp file creates when it populates our RDS instance with information


## Startup
Now that AWS CLI is configured and environment variables are created, run AWS\_Database\_Start.py to create your AWS RDS instance database. This should run every other setup script in sequence. Be aware that after the database .dmp file is downloaded there will be a password prompt required before pg_restore can construct the database.

**Disclaimer:**

* Database data takes approximately **1-7 minute(s)** to download depending on the internet connection.
* Populating the database could take up to approximately **35 minutes** with this instance configuration.
* AWS database instance size default is set to 20 gigabytes, the database as of July 16th, 2019 takes up about **10.3 gigabytes** of space after loaded onto the instance.