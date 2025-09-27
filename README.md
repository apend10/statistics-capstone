# FBref Scraper

This project contains scripts to scrape data from [FBref](https://fbref.com/) using Python and `curl_cffi` to bypass Cloudflare protections. It is split into two main components.

---
## 1. get_table_ids.py
Returns the table_ids of all the tables seen on a FBREF page with a specified URL.

Instructions

1. Get a link from FBREF where tables are present.
ex: "https://fbref.com/en/comps/9/2025-2026/stats/2025-2026-Premier-League-Stats"

2. Update the url variable with the link
3. Run the script to get the table names that are present on the webpage. 
4. They will be printed in the terminal and can be used in other scripts to scrape specific tables.

## 2. scrape_fbref.py

Inputs:
table_id: specific table ID to extract (e.g., 'stats_standard')
year_start: starting year for scraping (e.g., 2017)
year_end: ending year for scraping (e.g., 2025)

Note as of September 26 2025:
2017 represents the 2017-18 season! This means we cant say 2026 as the end year since 2026-27 season hasn't started yet!

Outputs:
The csv file with the scraped data is saved in the 'results' directory with the name format '{table_id}_{year_start}-{year_start+1}_to_{year_end+1}.csv'

---
## Running the Code

#### 1. Create a pyenv
> pyenv local 3.10.1

#### 2. Install all the required packages. 
> ~/.pyenv/versions/3.10.1/bin/python -m pip install --upgrade pip
> ~/.pyenv/versions/3.10.1/bin/python -m pip install curl_cffi pandas beautifulsoup4

#### 3. Run each file as you wish. 
> ~/.pyenv/versions/3.10.1/bin/python /path/to/get_table_ids.py
> ~/.pyenv/versions/3.10.1/bin/python /path/to/scrape_fbref.py