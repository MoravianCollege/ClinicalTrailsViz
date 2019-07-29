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
  library(scales)
}, error = function(e) {
  install.packages("scales")
  library(scales)
})

# Connect to AACT database
drv <- dbDriver('PostgreSQL')
con <- dbConnect(drv,
                 dbname=Sys.getenv("dbname"),
                 host=Sys.getenv("host"),
                 port=5432,
                 user=Sys.getenv("userid"),
                 password=Sys.getenv("userpass")
)

# Make ctgov schema public
dbExecute(con, "SET search_path TO ctgov,public")

# Retrieves data on the number of completed 'Parkinson Disease' trials per study type"
study_types_parkinsons <- dbGetQuery(con, "SELECT * FROM studies NATURAL JOIN browse_conditions WHERE downcase_mesh_term='parkinson disease' AND overall_status='Completed'")
study_types_grouped <- group_by(study_types_parkinsons, study_type)
View(summarise(study_types_grouped, count=n()), "Study Type & Parkinson's")

# Plots a bar chart displaying the number of Parkinson Disease trials per study type
x <- summarise(study_types_grouped, count = n())
x$study_type <- factor(x$study_type, levels = x$study_type[order(-x$count)])
plot <- ggplot(data=x, aes(x=study_type, y=count)) + geom_bar(stat="identity") +
  labs(title = "Total Number of Completed 'Parkinson Disease' Trials by Study Type",
       caption = "The histogram above visulaizes the number of completed 'Parkinson Disease' trials per study type") + 
  theme(plot.title = element_text(hjust = 0.5),
        plot.caption=element_text(hjust=0.5, vjust=0.5))
plot + scale_y_continuous(labels = comma)

