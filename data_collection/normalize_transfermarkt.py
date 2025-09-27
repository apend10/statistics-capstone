import pandas as pd

df = pd.read_csv("transfermarkt_data_raw.csv")

max_values_per_year = df.groupby('Year')['Total_Market_Value'].max()

df['normalized_total_market_value'] = df.apply(
    lambda row: row['Total_Market_Value'] / max_values_per_year[row['Year']], 
    axis=1
)

df.to_csv("transfermarkt_data_normalized.csv", index=False)