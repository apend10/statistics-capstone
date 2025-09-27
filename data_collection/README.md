## Retracing My Steps
Here is everything we did to get the data we got from FBREF. 
The goal is to get all the data we need for our project first from FBREF and then from Transfermarkt. 

### FBREF

##### Link 1: https://fbref.com/en/comps/9/2025-2026/stats/2025-2026-Premier-League-Stats

Since this contains general stats and the main thing here is XG metrics for teams, we got data from this site since 2017-18 up til 2025-26. XG metrics only began after 2017-18!

> Table: stats_squads_standard_for
> Result: results/stats_squads_standard_for_2017-2018_to_2025-2026.csv

I also wanted to get player stats of all players for each year since 1992/93

> Table: stats_standard
> Result: results/stats_standard_1992-1993_to_2025-2026.csv

##### Link 2: https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats
I need to get the Premier League table for every season since 1992-93. 

> Table: results2024-202591_overall
> Result: /results/league_table_1992-1993_to_2025-2026.csv

Note: In this case, the table name is linked with the year. This will obviously have to be handled differently. I had to make some small changes to the code!
Note 2: I renamed the result file since the table name obviously changes for each year.

##### Link 3: https://fbref.com/en/comps/9/1992-1993/schedule/1992-1993-Premier-League-Scores-and-Fixtures
I need to get the result of every Premier League game since 1992-93.

> Table: sched_1992-1993_9_1
> Result: results/fixtures_1992-1993_to_2025-2026.csv

Note: In this case, the table name is linked with the year. This will obviously have to be handled differently. I had to make some small changes to the code!
Note 2: I renamed the result file since the table name obviously changes for each year.

##### Link 4: https://fbref.com/en/comps/9/2017-2018/gca/2017-2018-Premier-League-Stats
I want to get attacking stats in the form of goal creating actions. 
Data exists only since 2017/18.

First for each team
> Table: stats_squads_gca_for
> Result: /results/stats_squads_gca_for_2017-2018_to_2025-2026.csv

And then for each player
> Table: stats_gca
> Result: /results/stats_gca_2017-2018_to_2025-2026.csv

##### Link 5: https://fbref.com/en/comps/9/2017-2018/defense/2017-2018-Premier-League-Stats
I want to get defensive stats.
Data exists only since 2017/18.

First for each team
> Table: stats_squads_defense_for
> Result: results/stats_squads_defense_for_2017-2018_to_2025-2026.csv

And then for each player
> Table: stats_defense
> Result: results/stats_defense_2017-2018_to_2025-2026.csv

#### Link 6: https://fbref.com/en/comps/9/2017-2018/keepers/2017-2018-Premier-League-Stats
I also want to get goalkeeping stats. 
Data exists only since 2017/18. 

First for each team
> Table: stats_squads_keeper_for
> Result: results/stats_squads_keeper_for_2017-2018_to_2025-2026.csv

And then for each player
> Table: stats_keeper
> Result: results/stats_keeper_2017-2018_to_2025-2026.csv

### Transfermarkt

This code works a lot different than FBref due to a more relaxed monitoring service. This code can simply be run normally. 

> python3 scrape_transfermarkt.py

The primary purpose of getting this data is to monitor the strength of each squad by the size of it and the financial strength of each team (sum of the values of all their players). However, an important realization is to normalize the market values of all the teams which is done in normalize_transfermarkt.py