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

# Query database for list of why_stopped reasons that aren't equal to 'Other' and their clinical trial condition
stop <- dbGetQuery(con, "select why_stopped_table.nct_id, why_stopped_table.stop_reason, condition_type.condition_category FROM why_stopped_table JOIN condition_type ON why_stopped_table.nct_id = condition_type.nct_id WHERE why_stopped_table.stop_reason != 'Other'")

# Plot a proportional analysis of trial stop reasons vs trial conditions
#ggplot(df, aes(x = stop.stop_reason, y = ..prop.., group = stop.condition_category)) + geom_bar(aes(fill = stop.condition_category), position = "dodge2") + labs(title="Proportional Analysis of Trial Stop Reason vs Trial Condition Type") + xlab("Stop Reason") + ylab("Proportion (%)") + scale_fill_discrete(name = "Condition Type")
#ggplot(df, aes(x = stop.stop_reason, y = ..prop.., group = stop.condition_category)) + geom_bar(aes(fill = stop.condition_category), position = "dodge2") + labs(title="Proportional Analysis of Trial Stop Reason vs Trial Condition Type") + xlab("Stop Reason") + ylab("Proportion (%)") + scale_fill_discrete(name = "Condition Type") + coord_flip()
ggplot(df, aes(x = stop.stop_reason, y = ..prop.., group = stop.condition_category)) + geom_bar(aes(fill = stop.condition_category), position = "dodge2") + labs(title="Proportional Analysis of Trial Stop Reason vs Trial Condition Type") + xlab("Stop Reason") + ylab("Proportion (%)") + scale_fill_discrete(name = "Condition Type") + scale_x_discrete(limits = c("Enrollment","Accrual","Sponsor or PI decision","Lack of funding","Ineffective or futile","Safety","Business Decision","Administrative decision","Feasibility reasons","Logistic Reasons","Toxicity")) + coord_flip() + scale_y_continuous(labels=scales::percent)
#ggplot(df, aes(x = stop.stop_reason, y = ..prop.., group = stop.condition_category)) + geom_bar(aes(fill = stop.condition_category), position = "dodge2") + labs(title="Proportional Analysis of Trial Stop Reason vs Trial Condition Type") + xlab("Stop Reason") + ylab("Proportion (%)") + scale_fill_discrete(name = "Condition Type") + scale_x_discrete(limits = c("Enrollment","Accrual","Sponsor or PI decision","Lack of funding","Ineffective or futile","Safety","Business Decision","Administrative decision","Feasibility reasons","Logistic Reasons","Toxicity")) + coord_flip() + scale_y_continuous(labels=scales::percent) + facet_wrap(~ stop.condition_category, ncol=4)
