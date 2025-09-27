"""
get_table_ids.py

Returns the table_ids of all the tables seen on a FBREF page with a specified URL.

Instructions

1. Get a link from FBREF where tables are present.
ex: "https://fbref.com/en/comps/9/2025-2026/stats/2025-2026-Premier-League-Stats"

2. Update the url variable with the link
3. Run the script to get the table names that are present on the webpage. 
4. They will be printed in the terminal and can be used in other scripts to scrape specific tables.
"""

import os
import curl_cffi
import pandas as pd
from bs4 import BeautifulSoup
import time

session = curl_cffi.Session()  # reuse across calls

def list_table_ids(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = session.get(url, headers=headers, impersonate="chrome120")
        if response.status_code != 200:
            print(f"Failed to fetch: {response.status_code}")
            return []

        html = response.text.replace("<!--", "").replace("-->", "")
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")  # find all tables
        table_ids = [table.get("id") for table in tables if table.get("id")]
        return table_ids

    except Exception as e:
        print(f"Error: {e}")
        return []

# Usage:
url = "https://fbref.com/en/comps/9/1992-1993/schedule/1992-1993-Premier-League-Scores-and-Fixtures"
table_ids = list_table_ids(url)
print(table_ids)

# ~/.pyenv/versions/3.10.1/bin/python /Users/apendela10/STAT482/statistics-capstone/data_collection/get_table_ids.py