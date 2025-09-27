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