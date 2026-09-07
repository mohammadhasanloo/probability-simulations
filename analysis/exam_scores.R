# Exam scores: how the three subjects are distributed, and who scores what.

library(ggplot2)

# Paths are resolved from the repository root so the script runs from anywhere.
root <- Sys.getenv("PROJECT_ROOT", unset = getwd())
scores <- read.csv(file.path(root, "data", "exam_scores.csv"))

subjects <- c("math_score", "reading_score", "writing_score")

summary_table <- do.call(rbind, lapply(subjects, function(subject) {
  values <- scores[[subject]]
  data.frame(
    subject = subject,
    mean = mean(values),
    sd = sd(values),
    median = median(values),
    # Shapiro-Wilk asks whether the values could have come from a normal
    # distribution. A small p-value says they could not.
    shapiro_p = shapiro.test(values)$p.value
  )
}))
print(summary_table, row.names = FALSE)

write.csv(summary_table, file.path(root, "results", "exam_score_summary.csv"),
          row.names = FALSE)

long <- data.frame(
  subject = rep(subjects, each = nrow(scores)),
  score = unlist(scores[subjects], use.names = FALSE),
  gender = rep(scores$gender, times = length(subjects))
)

distributions <- ggplot(long, aes(x = score, fill = gender)) +
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.55) +
  facet_wrap(~ subject) +
  labs(title = "Score distribution by subject and gender",
       x = "score", y = "students") +
  theme_minimal()

quantiles <- ggplot(long, aes(sample = score, colour = subject)) +
  stat_qq() +
  stat_qq_line(colour = "black", linewidth = 0.4) +
  facet_wrap(~ subject) +
  labs(title = "Normal quantile plots",
       x = "theoretical quantile", y = "observed score") +
  theme_minimal() +
  theme(legend.position = "none")

by_group <- ggplot(scores, aes(x = race, y = math_score, colour = gender)) +
  geom_boxplot() +
  labs(title = "Maths score by group and gender", x = NULL, y = "maths score") +
  theme_minimal()

ggsave(file.path(root, "docs", "score_distributions.png"), distributions,
       width = 9, height = 4, dpi = 130)
ggsave(file.path(root, "docs", "score_quantiles.png"), quantiles,
       width = 9, height = 4, dpi = 130)
ggsave(file.path(root, "docs", "score_by_group.png"), by_group,
       width = 8, height = 4.5, dpi = 130)
