#Q4_Part4
library(ggplot2)
library(tidyverse)
library(dplyr)
grades <- read.csv("grades.csv")

#Parta
#blue for males
males_grades = grades[grades $ gender == 'male',]
males_grades_plot = ggplot(males_grades, aes(x = writing_score)) + geom_histogram(fill = "blue", binwidth = 0.5)
males_grades_plot

#pink for females
females_grades = grades[grades $ gender == 'female',]
females_grades_plot = ggplot(females_grades, aes(x = writing_score)) + geom_histogram(fill = "pink", binwidth = 0.5)
females_grades_plot

#Partb
#red for math score distribution
math_score_distribution <- ggplot(grades) +
  stat_qq(aes(sample = math_score), colour = "red")

math_score_distribution

#blue for math score distribution
reading_score_distribution <- ggplot(grades) +
  stat_qq(aes(sample = reading_score), colour = "blue")

reading_score_distribution

#green for math score distribution
writing_score_distribution <- ggplot(grades) +
  stat_qq(aes(sample = writing_score), colour = "green")

writing_score_distribution

#Partc
math_score_box_plot <- ggplot(grades, aes(x = race, y = math_score, color = gender)) + geom_boxplot()

math_score_box_plot

students_marks_means <- grades
students_marks_means["average"] = (students_marks_means["reading_score"] + students_marks_means["writing_score"] + students_marks_means["math_score"]) / 3

students_marks_means_plot <- ggplot(students_marks_means) + geom_bar(aes(x = parents_education, y = average, fill = parents_education), stat = "summary", fun = "mean")

students_marks_means_plot
