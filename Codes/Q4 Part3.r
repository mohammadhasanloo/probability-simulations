#Q4_Part3
library(ggplot2)
library(tidyverse)
library(dplyr)
students_performance <- read.csv("StudentsPerformance.csv")

#Parta
students_performance_sample <- ggplot(students_performance, aes(x = G1, y = (G1 + G2 + G3)/3)) + geom_point(col = "black")
students_performance_sample

#partc
correlation_coefficient = cor(students_performance["G1"], students_performance["G1"] + students_performance["G2"] + students_performance["G3"]/3)
correlation_coefficient

#Parta
students_performance_sample <- ggplot(students_performance, aes(x = failures, y = (G1 + G2 + G3)/3)) + geom_point(col = "black")
students_performance_sample

#partc
correlation_coefficient = cor(students_performance["failures"], students_performance["G1"] + students_performance["G2"] + students_performance["G3"]/3)
correlation_coefficient
