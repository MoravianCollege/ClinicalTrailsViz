# ClinicalTrialsViz

-

### Setting up system environment variables:

To access the clinical trials database, you will be prompted with a username and password to connect. If you have not made an AACT account yet, you can sign up [here.](https://aact.ctti-clinicaltrials.org/users/sign_up) Before using the files in this repository, you must do the following:

* Go to the home directory of your terminal `cd $HOME`

* Create a new file called __.Renviron__ `sudo nano .Renviron`

* Inside the file write your username and password environment variables with your AACT account login information:

``` 
userid = "'your database account username'"
userpass = "'your database account password'"

```

* Save and exit nano pressing the keys `ctrl+c, ctrl+x, y, enter`

* Restart your R studio application to ensure environment variables are processed

* Now you may use the scripts available in the repository, these environment variables will be referenced later using the syntax Sys.getenv()

-

### Connecting to the database

* First-time startup enter the command (this command will only ever need to be entered one time) `install.packages("RPostgreSQL")`

* Then you must access the RPostgreSQL library to use the commands `library(RPostgreSQL)`

* Initialize database driver `drv <- dbDriver('PostgreSQL')`

* Connect to database with user environment variables

```
con <- dbConnect(drv,    dbname="aact",    host="aact-db.ctti-clinicaltrials.org",    port=5432,    user=Sys.getenv("userid"),    password=Sys.getenv("userpass"))
```

* Test that your connection is valid with a sample database query command `aact_sample <- dbGetQuery(con, "select distinct study_type from studies")`

* If you are still having issues reference the AACT website [here.](https://aact.ctti-clinicaltrials.org/r)