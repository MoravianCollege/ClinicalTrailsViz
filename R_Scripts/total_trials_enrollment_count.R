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

# Query database for enrollment of completed trials
completed <- dbGetQuery(con, "SELECT enrollment, overall_status FROM Studies WHERE overall_status = 'Completed'")

# Summarize the total number of trials with the same enrollment count
completed <- completed %>%
  group_by(enrollment) %>% 
  summarize(count = n())

# Create histogram to visualize the number of people enrolled in each completed trial
completed %>% 
  filter(enrollment <= 20000) %>% 
  ggplot() + geom_histogram(mapping = aes(enrollment), bins = 200, fill = 'black')
