# Premier League Prediction Model

## Table of Contents
	1.	Models
	2.	Data Collection and Exploratory Data Analysis
	•	get_table_ids.py
	•	scrape_fbref.py
	3.	Running the Code

⸻

### Models

Within the model-1-multi-lin-reg folder you will find a basic multiple linear regression model. One version is fit with PCA components, and one is fit with normalized features. It is implemented as a Jupyter notebook.

Next steps will include a Monte Carlo simulation and a neural network model.

⸻

### Data Collection and Exploratory Data Analysis

This project contains scripts to scrape data from FBref using Python and curl_cffi to bypass Cloudflare protections. It is split into two main components.

1. get_table_ids.py

Returns the table_ids of all tables on a FBref page with a specified URL.

Instructions:
	1.	Get a link from FBref where tables are present, e.g.:
https://fbref.com/en/comps/9/2025-2026/stats/2025-2026-Premier-League-Stats
	2.	Update the url variable with the link.
	3.	Run the script to get the table names present on the webpage.
	4.	Table names will be printed in the terminal and can be used in other scripts to scrape specific tables.

2. scrape_fbref.py

Inputs:
	•	table_id: specific table ID to extract (e.g., 'stats_standard')
	•	year_start: starting year for scraping (e.g., 2017)
	•	year_end: ending year for scraping (e.g., 2025)

Note (as of September 26, 2025):
2017 represents the 2017-18 season. The 2026-27 season has not started yet, so year_end cannot be 2026.

Outputs:
The CSV file with the scraped data is saved in the results directory with the name format:
{table_id}_{year_start}-{year_start+1}_to_{year_end+1}.csv

⸻

### Running the Code

1. Create a pyenv

pyenv local 3.10.1

2. Install required packages

~/.pyenv/versions/3.10.1/bin/python -m pip install --upgrade pip
~/.pyenv/versions/3.10.1/bin/python -m pip install curl_cffi pandas beautifulsoup4

3. Run the scripts

~/.pyenv/versions/3.10.1/bin/python /path/to/get_table_ids.py
~/.pyenv/versions/3.10.1/bin/python /path/to/scrape_fbref.py