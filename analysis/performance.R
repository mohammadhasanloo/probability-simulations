# School performance: what predicts a student's average grade?
#
# The three period grades G1, G2 and G3 are averaged into one score, and each
# candidate predictor is plotted against it and correlated with it.

library(ggplot2)

# Paths are resolved from the repository root so the script runs from anywhere.
root <- Sys.getenv("PROJECT_ROOT", unset = getwd())
students <- read.csv(file.path(root, "data", "student_performance.csv"))

# The parentheses matter. Without them this is G1 + G2 + G3/3, which is a
# different quantity from the average and correlates differently with it.
students$average <- (students$G1 + students$G2 + students$G3) / 3

predictors <- c("G1", "failures", "absences", "studytime", "goout", "health")

correlations <- data.frame(
  predictor = predictors,
  correlation = sapply(predictors, function(name)
    cor(students[[name]], students$average))
)
correlations <- correlations[order(-abs(correlations$correlation)), ]
print(correlations, row.names = FALSE)

write.csv(correlations,
          file.path(root, "results", "performance_correlations.csv"),
          row.names = FALSE)

scatter <- ggplot(students, aes(x = G1, y = average)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", formula = y ~ x, colour = "#1f6feb") +
  labs(title = "First period grade against the term average",
       x = "G1", y = "average of G1, G2 and G3") +
  theme_minimal()

failures <- ggplot(students, aes(x = factor(failures), y = average)) +
  geom_boxplot(fill = "#d1495b", alpha = 0.5) +
  labs(title = "Past failures against the term average",
       x = "previous failures", y = "average of G1, G2 and G3") +
  theme_minimal()

ggsave(file.path(root, "docs", "performance_g1.png"), scatter,
       width = 7, height = 4.5, dpi = 130)
ggsave(file.path(root, "docs", "performance_failures.png"), failures,
       width = 7, height = 4.5, dpi = 130)
