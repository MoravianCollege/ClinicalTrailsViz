# Query gender and display number of trials in a table
parkinsons <- dbGetQuery(con, "select * from studies natural join browse_conditions where downcase_mesh_term='parkinson disease'")
parkinsons_grouped <- group_by(parkinsons, nct_id)
View(summarise(parkinsons_grouped, count=n()), "Number of Studies for Mesh Term")

# Obtains all studies where the mesh term is 'Parkinson Disease' (there exists other mesh terms that include PD)
# Retrieves the 'brief title' associated with each of these trials
descriptions <- dbGetQuery(con, "select * from studies natural join browse_conditions where downcase_mesh_term='parkinson disease'")
descriptions_grouped <- group_by(descriptions, brief_title)
View(summarise(descriptions_grouped, count=n()), "Descriptions")

# Retrieves data concerning the mesh term 'Parkinson Disease' and the study_type for each trial"
study_types_parkinsons <- dbGetQuery(con, "select * from studies natural join browse_conditions where downcase_mesh_term='parkinson disease'")
study_types_grouped <- group_by(study_types_parkinsons, study_type)
View(summarise(study_types_grouped, count=n()), "Study Type & Parkinson's")

# Plots a bar chart displaying the number of Parkinson Disease trials per study type
x <- summarise(study_types_grouped, count = n())
x$study_type <- factor(x$study_type, levels = x$study_type[order(-x$count)])
plot <- ggplot(data=x, aes(x=study_type, y=count)) + geom_bar(stat="identity")
plot + scale_y_continuous(labels = comma)