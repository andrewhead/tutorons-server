# Load data from CSV
d = read.csv('web_affordances.csv')

results = subset(d, grepl("Verdict", Resource))
results_long <- reshape(results, 
  idvar="Resource",
  direction="long",
  varying=names(results[2:7]),
  times=names(results[2:7]),
  timevar="Task",
  v.names="Valid")

keeps = c("Resource", "Task", "Valid")
results_small = results_long[keeps]
rownames(results_small) <- NULL
results_small$Resource = gsub(" Verdict", "", results_small$Resource)
write.csv(results_small, 'web_affordances_long.csv', row.names=FALSE)