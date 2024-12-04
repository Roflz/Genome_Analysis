# Load necessary libraries
library(ggplot2)
library(readr)

# Load the data
data <- read_csv("genomic_annotations.csv")

# Summary statistics
summary(data)

# Visualization: Length of Features
data <- data[data$`Feature Type` != "source", ]

# Bar plot of feature types
ggplot(data, aes(x = `Feature Type`)) +
  geom_bar(fill = "steelblue") +
  theme_minimal() +
  labs(title = "Distribution of Feature Types", x = "Feature Type", y = "Count")

# Feature Length Distribution (Histogram), All Features
ggplot(data, aes(x = End - Start, color = `Feature Type`)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of Feature Lengths", x = "Feature Length", y = "Frequency")

# Gene Length Distribution (Histogram)
ggplot(data[data$`Feature Type` == "gene", ], aes(x = End - Start)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of Gene Lengths", x = "Gene Length (bp)", y = "Frequency")

# CDS Length Distribution (Histogram)
ggplot(data[data$`Feature Type` == "CDS", ], aes(x = End - Start)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of CDS Lengths", x = "Gene Length (bp)", y = "Frequency")

# misc_feature Length Distribution (Histogram)
ggplot(data[data$`Feature Type` == "misc_feature", ], aes(x = End - Start)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of misc_feature Lengths", x = "Gene Length (bp)", y = "Frequency")

# mobile_element Length Distribution (Histogram)
ggplot(data[data$`Feature Type` == "mobile_element", ], aes(x = End - Start)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of mobile_element Lengths", x = "Gene Length (bp)", y = "Frequency")

# ncRNA Length Distribution (Histogram)
ggplot(data[data$`Feature Type` == "ncRNA", ], aes(x = End - Start)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of ncRNA Lengths", x = "Gene Length (bp)", y = "Frequency")

# rRNA Length Distribution (Histogram)
ggplot(data[data$`Feature Type` == "rRNA", ], aes(x = End - Start)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of rRNA Lengths", x = "Gene Length (bp)", y = "Frequency")

# tRNA Length Distribution (Histogram)
ggplot(data[data$`Feature Type` == "tRNA", ], aes(x = End - Start)) +
  geom_histogram(fill = "steelblue", binwidth = 100) +
  theme_minimal() +
  labs(title = "Distribution of tRNA Lengths", x = "Gene Length (bp)", y = "Frequency")

# Scatter plot of feature lengths by type
selected_features <- c("tRNA", "gene", "ncRNA", "rRNA")
ggplot(data[data$`Feature Type` %in% selected_features, ], aes(x = Start, y = End, color = `Feature Type`)) +
  geom_point() +
  theme_minimal() +
  labs(title = "Feature Lengths by Type", x = "Start Position", y = "End Position")

ggplot(data, aes(x = Start)) +
  geom_density(fill = "lightblue", alpha = 0.5) +
  theme_minimal() +
  labs(title = "Feature Density Across Genome", x = "Genomic Position", y = "Density")