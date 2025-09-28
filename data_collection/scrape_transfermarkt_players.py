import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from fake_useragent import UserAgent

# Function to scrape players for a given team URL
def scrape_transfermarkt_players(url):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    for attempt in range(10):
        try:
            page = requests.get(url, headers=headers, timeout=15)
            if page.status_code == 200:
                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(random.randint(5, 15))
    else:
        print(f"Failed to get URL: {url}")
        return pd.DataFrame(columns=["Name", "Position", "Market Value"])

    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.select("table.items > tbody > tr")

    data = []
    for row in rows:
        name_cell = row.find("td", {"class": "hauptlink"})
        val_cell = row.find("td", {"class": "rechts hauptlink"})
        pos_cell = row.find("td", {"class": "posrela"})

        if name_cell and val_cell and pos_cell:
            name = name_cell.text.strip()

            position_map = {
                "Goalkeeper": "Goalkeeper",
                "Left-Back": "Left-Back",
                "Centre-Back": "Centre-Back",
                "Right-Back": "Right-Back",
                "Defensive Midfield": "Defensive Midfield",
                "Central Midfield": "Central Midfield",
                "Attacking Midfield": "Attacking Midfield",
                "Left Winger": "Left Winger",
                "Right Winger": "Right Winger",
                "Centre-Forward": "Centre-Forward"
            }

            position = "Other"
            for key in position_map:
                if key in pos_cell.text:
                    position = position_map[key]
                    break

            value = val_cell.text.strip()
            data.append([name, position, value])

    return pd.DataFrame(data, columns=["Name", "Position", "Market Value"])


# Dictionary of teams & URLs
teams_dict = {
    "chelsea fc": "https://www.transfermarkt.us/chelsea-fc/kader/verein/631/saison_id/",
    "manchester united": "https://www.transfermarkt.us/manchester-united/kader/verein/985/saison_id/",
    "arsenal fc": "https://www.transfermarkt.us/arsenal-fc/kader/verein/11/saison_id/",
    "liverpool fc": "https://www.transfermarkt.us/liverpool-fc/kader/verein/31/saison_id/",
    "tottenham hotspur": "https://www.transfermarkt.us/tottenham-hotspur/kader/verein/148/saison_id/",
    "newcastle united": "https://www.transfermarkt.us/newcastle-united/kader/verein/762/saison_id/",
    "birmingham city": "https://www.transfermarkt.us/birmingham-city/kader/verein/337/saison_id/",
    "middlesbrough fc": "https://www.transfermarkt.us/middlesbrough-fc/kader/verein/641/saison_id/",
    "manchester city": "https://www.transfermarkt.com/manchester-city/kader/verein/281/saison_id/",
    "southampton fc": "https://www.transfermarkt.com/southampton-fc/kader/verein/180/saison_id/",
    "aston villa": "https://www.transfermarkt.com/aston-villa/kader/verein/405/saison_id/",
    "everton fc": "https://www.transfermarkt.com/everton-fc/kader/verein/29/saison_id/",
    "blackburn rovers": "https://www.transfermarkt.com/blackburn-rovers/kader/verein/164/saison_id/",
    "fulham fc": "https://www.transfermarkt.com/fulham-fc/kader/verein/931/saison_id/",
    "portsmouth fc": "https://www.transfermarkt.com/portsmouth-fc/kader/verein/1020/saison_id/",
    "bolton wanderers": "https://www.transfermarkt.com/bolton-wanderers/kader/verein/355/saison_id/",
    "charlton athletic": "https://www.transfermarkt.com/charlton-athletic/kader/verein/358/saison_id/",
    "west bromwich albion": "https://www.transfermarkt.com/west-bromwich-albion/kader/verein/984/saison_id/",
    "crystal palace": "https://www.transfermarkt.com/crystal-palace/kader/verein/873/saison_id/",
    "norwich city": "https://www.transfermarkt.com/norwich-city/kader/verein/1123/saison_id/",
    "west ham united": "https://www.transfermarkt.com/west-ham-united/kader/verein/379/saison_id/",
    "wigan athletic": "https://www.transfermarkt.com/wigan-athletic/kader/verein/1071/saison_id/",
    "sunderland afc": "https://www.transfermarkt.com/sunderland-afc/kader/verein/289/saison_id/",
    "sheffield united": "http://transfermarkt.com/sheffield-united/kader/verein/350/saison_id/",
    "watford fc": "https://www.transfermarkt.com/watford-fc/kader/verein/1010/saison_id/",
    "reading fc": "https://www.transfermarkt.com/reading-fc/kader/verein/1032/saison_id/",
    "derby county": "https://www.transfermarkt.com/derby-county/kader/verein/22/saison_id/",
    "hull city": "https://www.transfermarkt.com/hull-city/kader/verein/3008/saison_id/",
    "stoke city": "https://www.transfermarkt.com/stoke-city/kader/verein/512/saison_id/",
    "wolverhampton wanderers": "https://www.transfermarkt.com/wolverhampton-wanderers/kader/verein/543/saison_id/",
    "burnley fc": "https://www.transfermarkt.com/burnley-fc/kader/verein/1132/saison_id/",
    "blackpool fc": "https://www.transfermarkt.com/blackpool-fc/kader/verein/1181/saison_id/",
    "queens park rangers": "https://www.transfermarkt.com/queens-park-rangers/kader/verein/1039/saison_id/2025/",
    "swansea city": "https://www.transfermarkt.com/swansea-city/kader/verein/2288/saison_id/",
    "cardiff city": "https://www.transfermarkt.com/cardiff-city/kader/verein/603/saison_id/",
    "leicester city": "https://www.transfermarkt.com/leicester-city/kader/verein/1003/saison_id/",
    "afc bournemouth": "https://www.transfermarkt.com/afc-bournemouth/kader/verein/989/saison_id/",
    "brighton & hove albion": "https://www.transfermarkt.com/brighton-amp-hove-albion/kader/verein/1237/saison_id/",
    "huddersfield town": "https://www.transfermarkt.com/huddersfield-town/kader/verein/1110/saison_id/",
    "leeds united": "https://www.transfermarkt.com/leeds-united/kader/verein/399/saison_id/",
    "brentford fc": "https://www.transfermarkt.com/brentford-fc/kader/verein/1148/saison_id/",
    "nottingham forest": "https://www.transfermarkt.com/nottingham-forest/kader/verein/703/saison_id/",
    "luton town": "https://www.transfermarkt.com/luton-town/kader/verein/1031/saison_id/",
    "ipswich town": "https://www.transfermarkt.com/ipswich-town/kader/verein/677/saison_id/"
}

# Function to generate URL for a team and season
def get_url(team, year):
    return teams_dict[team] + str(year) + "/plus/1"

# Loop over all teams and seasons
if __name__ == "__main__":
    td = pd.read_csv("results/transfermarkt_data_raw.csv")
    data = pd.DataFrame(columns=["Name", "Position", "Market Value", "Year", "Team"])
    data.to_csv("results/transfermarkt_data_players.csv", index=False)
    
    for year in range(2004, 2026):
        print("Starting year:", year)
        for team in td[td["Year"]==year]["Team"]:
            url = get_url(team, year)

            data = scrape_transfermarkt_players(url)

            data["Year"] = year
            data["Team"] = team

            data.to_csv("results/transfermarkt_data_players.csv", mode='a', header=False, index=False)
            
            print(random.randint(1, 20) * '-', f"got data for {team} @ ({year}) with {len(data)} players")

            if len(data) == 0:
                print(url)

