df <- read.csv("/Users/apendela10/STAT482/statistics-capstone/r-modelling/mlr_data.csv")

# install.packages("leaps")
library(leaps)

# columns
# Team,Squad_Size,Average_Age,Number_of_Foreigners,Average_Market_Value,Total_Market_Value,Position,Goal_Difference,Points,Year,Squad_Size_Normalized_by_Avg,Squad_Size_Normalized_by_Max,Average_Age_Normalized_by_Avg,Average_Age_Normalized_by_Max,Number_of_Foreigners_Normalized_by_Avg,Number_of_Foreigners_Normalized_by_Max,Average_Market_Value_Normalized_by_Avg,Average_Market_Value_Normalized_by_Max,Total_Market_Value_Normalized_by_Avg,Total_Market_Value_Normalized_by_Max

# Based on our EDA in python, we found that features normalized by average are better correlated
# So lets remove all the features normalized by max and un-normalized features
# Un-normalized Features to keep: Team,Position,Goal_Difference,Points,Year,
# Normalized Features to keep: Squad_Size_Normalized_by_Avg,Average_Age_Normalized_by_Avg,Number_of_Foreigners_Normalized_by_Avg, Average_Market_Value_Normalized_by_Avg,Total_Market_Value_Normalized_by_Avg

df <- read.csv("/Users/apendela10/STAT482/statistics-capstone/r-modelling/transfermarkt_financial_final.csv")

# Fit best subset model — test all 2^5 - 1 = 31 possible combinations
fit <- regsubsets(
  Points ~ Squad_Size_Normalized_by_Avg + Average_Age_Normalized_by_Avg +
    Number_of_Foreigners_Normalized_by_Avg + Average_Market_Value_Normalized_by_Avg +
    Total_Market_Value_Normalized_by_Avg,
  data = df,
  nvmax = 5,            # number of predictors
  method = "exhaustive" # ensure full search
)

summary_fit <- summary(fit)

# Show metrics
summary_fit$adjr2
summary_fit$cp
summary_fit$bic

# Plots for selection metrics
plot(fit, scale = "adjr2")
plot(fit, scale = "bic")

# Identify the best model by Adjusted R² for different number of variables
best_index <- which.max(summary_fit$adjr2)
summary_fit$which[best_index, ]

length(summary_fit$adjr2)

