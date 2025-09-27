import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict

#Step1: create a variable called headers to tell the website that we are a browser and not a scraping tool
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }

#Global Variables
url = "https://www.transfermarkt.us/premier-league/startseite/wettbewerb/GB1/plus/?saison_id="

total_data = []

def match_names(fullnames, nicknames):
    mapping = defaultdict() #nickname : fullname

    #exhaustive pairing
    for i in range(len(nicknames)):
        all_names = nicknames[i].split()

        for j in range(len(fullnames)):
            match = True

            for k in all_names:
                if(k not in fullnames[j]):
                    match = False
            
            if(match):
                mapping[nicknames[i]] = fullnames[j]
    #edgecases
    mapping["qpr"] = "queens park rangers"
    mapping["man utd"] = "manchester united"
    
    #if the first three letters match
    for i in range(len(nicknames)):
        firstthree = ""
        if(nicknames[i] not in mapping.keys()):
            firstthree = nicknames[i][0:3]
        
            for j in range(len(fullnames)):
                if(firstthree in fullnames[j]):
                    mapping[nicknames[i]] = fullnames[j]
    return mapping

def collect_data(year):
    #Step 2: assigns the address of the page we need to scrape to a string
    link = url + str(year)

    try:
        # Step 3: uses the requests library to grab the code of a page and assign it to 'PageTree'
        pageTree = requests.get(link, headers=headers)

        # Step 4: parses the website code into html and we will be able to search through this for the data we want to extract
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        # Step 5: Extracting team names
        team_names_raw = pageSoup.find_all("td", {"class": "hauptlink no-border-links"})
        team_names = []
        for i in range(20):
            if(team_names_raw[i].text[len(team_names_raw[i].text)-1:len(team_names_raw[i].text)] == '\xa0'):
                team_names.append((team_names_raw[i].text[:len(team_names_raw[i].text)-2]).lower())
            else:
                team_names.append((team_names_raw[i].text[0:len(team_names_raw[i].text) - 1]).lower())
        
        #Step 6: Extracting Squad Size, Average Age, and Number of Foreigners
        #they are all stored in the "zentriert" class in the website
        squad_age_foreigners_raw = pageSoup.find_all("td", {"class": "zentriert"})
        squad_size = []
        average_age = []
        num_foreigners = []
        i = 4
        while(len(squad_size) < 20):
            squad_size.append(int(squad_age_foreigners_raw[i].text))
            i += 1
            average_age.append(float(squad_age_foreigners_raw[i].text))
            i += 1
            num_foreigners.append(int(squad_age_foreigners_raw[i].text))
            i += 2

        squad_age_foreigners_raw = squad_age_foreigners_raw[i:]

        #Step 7: Extracting Average Market Value and Total Market Value
        market_values_raw = pageSoup.find_all("td", {"class": "rechts"})
        average_market_value = [] #in millions
        total_market_value = [] #in millions
        i = 2
        while(len(average_market_value) < 20):
            #getting the average market value
            amv = market_values_raw[i].text
            if(amv[len(amv)-1:] == "m"):
                amv = float(amv[1:len(amv)-1])
            elif(amv[len(amv)-1:] == "k"):
                amv = float(amv[1:len(amv)-1]) * 0.001
            average_market_value.append(amv)

            #iterating
            i += 1

            #getting the total market value
            tmv = market_values_raw[i].text
            if(tmv[len(tmv) - 1:] == "n"):
                tmv = float(tmv[1:len(tmv) - 2]) * 1000
            elif(tmv[len(tmv) - 1:] == "m"):
                tmv = float(tmv[1:len(tmv) - 1])
            total_market_value.append(tmv)

            #iterating
            i += 1
            
        print("-- Year {year} --".format(year=year))
        print(f"    Team : {len(team_names)}")
        print(f"    Squad Size : {len(squad_size)}")
        print(f"    Average Age : {len(average_age)}")
        print(f"    Number of Foreigners : {len(num_foreigners)}")
        print(f"    Average Market Value : {len(average_market_value)}")
        print(f"    Total Market Value : {len(total_market_value)}")
        #create data 
        global data
        data = pd.DataFrame({'Team': team_names, 
                            'Squad_Size': squad_size, 
                            'Average_Age': average_age,
                            'Number_of_Foreigners': num_foreigners,
                            'Average_Market_Value': average_market_value,
                            'Total_Market_Value': total_market_value
                            })  

        #Step 8: Extracting Position
        positions_raw = pageSoup.find_all("td", {"class": "rechts hauptlink"})
        positions = []
        for i in range(len(positions_raw)):
                positions.append(int(positions_raw[i].text))

        ranking_table_raw = pageSoup.find_all("td", {"class": "no-border-links hauptlink"})
        print(ranking_table_raw)
        ranking_table = []
        for i in range(len(ranking_table_raw)):
            if(ranking_table_raw[i].text[len(ranking_table_raw[i].text)-2:len(ranking_table_raw[i].text)-1] == '\xa0'):
                ranking_table.append((ranking_table_raw[i].text[1:len(ranking_table_raw[i].text) - 2]).lower())
            else:
                ranking_table.append((ranking_table_raw[i].text[1:len(ranking_table_raw[i].text)-1]).lower())
        print(ranking_table)


        #Step 9: Get Goal Difference and Points
            #the rest of the league table is in the "zentriert" class
            #which was stored previously in squad_age_foreigners_raw
        tds = squad_age_foreigners_raw
        goal_difference = []
        points = []

        i = 0
        while i < len(tds) and len(points) < 20:
            team_cell = tds[i].find("img")
            if team_cell:  # Found a team cell
                # make sure there are at least 3 more <td> after this one
                if i + 3 < len(tds):

                    def safe_int(td):
                        try:
                            return int(td.text.strip())
                        except (ValueError, AttributeError):
                            return None

                    matches = safe_int(tds[i+1])
                    gd = safe_int(tds[i+2])
                    p = safe_int(tds[i+3])

                    if None not in (matches, gd, p):
                        goal_difference.append(gd)
                        points.append(p)
                i += 4
            else:
                i += 1

    except Exception as e:
        print(f"Issue collecting data for year {year}!")
        print(e)
        print("______________________________________________")
    
    print("-- Year {year} --".format(year=year))
    print(f"    Team : {len(ranking_table)}")
    print(f"    Position : {len(positions)}")
    print(f"    Goal Difference : {len(goal_difference)}")
    print(f"    Points : {len(points)}")
    global data2
    data2 = pd.DataFrame({'Team': ranking_table, 
                        'Position': positions, 
                        'Goal_Difference': goal_difference,
                        'Points': points})

    fullnames = data["Team"].tolist()
    nicknames = data2["Team"].tolist()

    mapping = match_names(fullnames, nicknames)
    
    for i in range(len(data2)):
        data2["Team"][i] = mapping[data2["Team"][i]]
    
    global output
    output = data.join(data2.set_index('Team'), on='Team')
    
    year = [year] * 20
    output["Year"] = year
    total_data.append(output)



print("This program will populate a df with data from start year to end year")
start_year = 2025#int(input("Enter start year: ")) #2004 - 2004/05
end_year = 2026#int(input("Enter end year: ")) #2023


while(start_year < end_year):
    collect_data(start_year)
    print(" --- Finished year", start_year, " --- ")
    start_year += 1

    total_df = pd.concat(total_data)
    total_df.to_csv("2.0/Data2.csv", index=False)


total_df = pd.concat(total_data)
total_df.to_csv("2.0/Data.csv", index=False)