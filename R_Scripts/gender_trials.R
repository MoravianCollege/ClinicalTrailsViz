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
                 dbname="aact",
                 host=Sys.getenv("host"),
                 port=5432,
                 user=Sys.getenv("userid"),
                 password=Sys.getenv("userpass")
)

# Make ctgov schema public
dbExecute(con, "SET search_path TO ctgov,public")

# Query gender and display number of completed trials in each in a table
studies_gender <- dbGetQuery(con, "SELECT * FROM studies NATURAL JOIN eligibilities WHERE overall_status='Completed' AND gender!=''")
studies_gender_grouped <- group_by(studies_gender, gender)
View(summarise(studies_gender_grouped, count=n()), "Gender")

# Creates a bar graph to represent the number of completed trials per gender
x <- summarise(studies_gender_grouped, count = n())
x$gender <- factor(x$gender, levels = x$gender[order(-x$count)])
plot <- ggplot(data=x, aes(x=gender, y=count)) + geom_bar(stat="identity")+ 
  labs(title = "Total Number of Completed Trials by Gender",
       caption = "The histogram above visualizes the number of completed trials per the gender of eligibility") + 
  theme(plot.title = element_text(hjust = 0.5),
        plot.caption=element_text(hjust=0.5, vjust=0.5))
plot + scale_y_continuous(labels = comma)
