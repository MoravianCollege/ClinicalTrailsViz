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
                 host="aact-db.ctti-clinicaltrials.org",
                 port=5432,
                 user=Sys.getenv("userid"),
                 password=Sys.getenv("userpass")
)

# Query intervention types and sum up amounts in a table
studies_intervention <- dbGetQuery(con, "select * from studies natural join interventions")
studies_intervention_grouped <- group_by(studies_intervention, intervention_type)
View(summarise(studies_intervention_grouped, count=n()), "Intervention Types")

# Create a bar graph to represent values in descending order
x <- summarise(studies_intervention_grouped, count = n())
x$intervention_type <- factor(x$intervention_type, levels = x$intervention_type[order(-x$count)])
plot <- ggplot(data=x, aes(x=intervention_type, y=count)) + geom_bar(stat="identity")

# Show graph without scientific notation on y axis
plot + scale_y_continuous(labels = comma)
