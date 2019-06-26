# Install or load libraries
tryCatch({
  library(RPostgreSQL)
}, error = function(e) {
  install.packages("RPPostgreSQL")
  library(RPPostgreSQL)
})
tryCatch({
  library(tidyverse)
}, error = function(e) {
  install.packages("tidyverse")
  library(tidyverse)
})
tryCatch({
  library(lubridate)
}, error = function(e) {
  install.packages("lubridate")
  library(lubridate)
})

# Connect to database
drv <- dbDriver('PostgreSQL')
con <- dbConnect(drv,
                 dbname="aact",
                 host=Sys.getenv("host"),
                 port=5432,
                 user=Sys.getenv("userid"),
                 password=Sys.getenv("userpass")
)

# Make ctgov schema public
dbExecute(con, "SET search_path TO ctgov,public")

# Query database for start date
starting_date <- dbGetQuery(con, "SELECT start_date FROM Studies")

# Split column into two and plot count of each month
starting_date %>% 
  mutate(start_month = month(start_date, label = TRUE), start_year = year(start_date)) %>%
  group_by(start_month) %>%
  arrange(start_month) %>%
  summarize(count = n(), na.rm = TRUE) %>% 
  filter(start_month != "") %>%
  ggplot() + geom_col(aes(start_month, count), color = "black", fill = 'white') + labs(title = "Total Number of Trials Started Each Month") + theme(plot.title = element_text(hjust = 0.5))
