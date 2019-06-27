# Install/load libraries
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

# Connect to the database
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

# Query database for enrollment of trials with the MESH term 'Parkinson Disease'
enroll_pd <- dbGetQuery(con, "SELECT enrollment, overall_status FROM studies NATURAL JOIN browse_conditions WHERE downcase_mesh_term='parkinson disease' AND overall_status='Completed'")

# Summarize the total number of trials with the same enrollment count
enroll_pd <- enroll_pd %>%
  group_by(enrollment) %>% 
  summarize(count = n())

# Display histogram of the number of people enrolled in a completed trial where MESH term is 'Parkinson Disease'
enroll_pd %>% 
  filter(enrollment <= 4000) %>% 
  ggplot() + geom_histogram(mapping = aes(enrollment), 
                            bins = 200, fill = 'black') + 
    labs(title = "Total Number of 'Parkinson Disease' Completed Trials by Enrollment Count", 
         caption = "The histogram above displays the enrollment numbers for each completed clinical trial that contain the MESH term 'Parkinson Disease'") + 
    theme(plot.title = element_text(hjust = 0.5),
        plot.caption=element_text(hjust=0.5, vjust=0.5))
