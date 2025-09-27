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
year_start = 1992
year_end = 2025
table_id = f"sched_{year_start}-{year_start+1}_9_1"

ys, ye = year_start, year_end  # for filename

#Main Execution
url = f"https://fbref.com/en/comps/9/{year_start}-{year_start+1}/schedule/{year_start}-{year_start+1}-Premier-League-Scores-and-Fixtures"
df = scrape_fbref_curl_cffi(url, table_id=table_id)

# Table Specific Mofidications (uncomment based on table_id if needed)
df.insert(0, 'Year', year_start)
year_start += 1

while year_start < year_end:
    url = f"https://fbref.com/en/comps/9/{year_start}-{year_start+1}/schedule/{year_start}-{year_start+1}-Premier-League-Scores-and-Fixtures"
    
    # Table Specific Mofidications (uncomment based on table_id if needed)
    table_id = f"sched_{year_start}-{year_start+1}_9_1"
    df_next = scrape_fbref_curl_cffi(url, table_id=table_id)

    # Table Specific Mofidications (uncomment based on table_id if needed)
    df_next.insert(0, 'Year', year_start) 
    
    # append each year to main df
    df = pd.concat([df, df_next], ignore_index=True)
    year_start += 1

    # Progress update
    print(f"Scraped up to year {year_start-1} for the {table_id} table")
    
    # Uncomment below for debugging purposes
    df.to_csv(f"results/inprogress.csv", index=False)

if df is not None:
    #print(df)
    os.makedirs("results", exist_ok=True)
    df.to_csv(f"results/{table_id}_{ys}-{ys+1}_to_{ye}-{ye+1}.csv", index=False)

'''
Notes for running and reproducing results: 
~/.pyenv/versions/3.10.1/bin/python /Users/apendela10/STAT482/statistics-capstone/data_collection/scrape_fbref.py

For Link 1 [2 Tables]
url = f"https://fbref.com/en/comps/9/{year_start}-{year_start+1}/stats/{year_start}-{year_start+1}-Premier-League-Stats"
table_id = stats_squads_standard_for
table_id = stats_standard

For Link 2 [1 Table]
url = f"https://fbref.com/en/comps/9/{year_start}-{year_start+1}/{year_start}-{year_start+1}-Premier-League-Stats"
table_id = f"results{year_start}-{year_start+1}91_overall"
df_next.insert(0, 'Year', year_start) IS NEEDED

For Link 3 [1 Table]
url = f"https://fbref.com/en/comps/9/{year_start}-{year_start+1}/schedule/{year_start}-{year_start+1}-Premier-League-Scores-and-Fixtures"
table_id = f"sched_{year_start}-{year_start+1}_9_1"
Table Specific Mofidications (uncomment based on table_id if needed)
df_next.insert(0, 'Year', year_start) IS NEEDED
table_id = f"sched_{year_start}-{year_start+1}_9_1"
'''