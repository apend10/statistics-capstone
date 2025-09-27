"""
scrape_fbref.py

Scrapes FBref using curl_cffi to bypass Cloudflare.

Inputs:
table_id: specific table ID to extract (e.g., 'stats_standard')
year_start: starting year for scraping (e.g., 2017)
year_end: ending year for scraping (e.g., 2025)

Note as of September 26 2025:
2017 represents the 2017-18 season! This means we cant say 2026 as the end year since 2026-27 season hasn't started yet!

Outputs:
The csv file with the scraped data is saved in the 'results' directory with the name format '{table_id}_{year_start}-{year_start+1}_to_{year_end+1}.csv'
"""

import os
import curl_cffi
import pandas as pd
from bs4 import BeautifulSoup
import time

session = curl_cffi.Session()  # reuse across calls

def scrape_fbref_curl_cffi(url, table_id=None):
    """
    Scrape FBref using curl_cffi to bypass Cloudflare
    table_id: specific table ID to extract (e.g., 'stats_standard')
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        time.sleep(2)  # Be respectful
        
        response = session.get(
            url,
            headers=headers,
            impersonate="chrome120"  # impersonate real browser
        )
        
        if response.status_code == 200:
            # Remove HTML comments that hide tables
            html = response.text.replace("<!--", "").replace("-->", "")
            
            if table_id:
                soup = BeautifulSoup(html, "html.parser")
                table = soup.find("table", {"id": table_id})
                if table:
                    dfs = pd.read_html(str(table))
                    return dfs[0]  # return first DataFrame
                else:
                    print(f"No table found with id={table_id}")
                    return None
            else:
                dfs = pd.read_html(html)
                return dfs  # list of DataFrames
        else:
            print(f"Failed to fetch: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None



# Main Parameters
table_id = "stats_standard"
year_start = 2017
year_end = 2025

#Main Execution
url = f"https://fbref.com/en/comps/9/{year_start}-{year_start+1}/stats/{year_start}-{year_start+1}-Premier-League-Stats"
df = scrape_fbref_curl_cffi(url, table_id=table_id)
df.insert(0, 'Year', year_start)
year_start += 1

while year_start < year_end:
    url = f"https://fbref.com/en/comps/9/{year_start}-{year_start+1}/stats/{year_start}-{year_start+1}-Premier-League-Stats"
    df_next = scrape_fbref_curl_cffi(url, table_id=table_id)
    df_next.insert(0, 'Year', year_start)
    df = pd.concat([df, df_next], ignore_index=True)
    year_start += 1

if df is not None:
    #print(df)
    os.makedirs("results", exist_ok=True)
    df.to_csv(f"results/{table_id}_{year_start}-{year_start+1}_to_{year_end+1}.csv", index=False)

# ~/.pyenv/versions/3.10.1/bin/python /Users/apendela10/STAT482/statistics-capstone/data_collection/scrape_fbref.py