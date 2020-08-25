# League of Legends Analytics

Python Dash App created to show advanced derived from Riot's League of Legends API.

## Parts
+ __pipeline__: Pull's data from Riot's Leauge of Legends API and inserts it into a Postgresql Database using Python.
+ __generate_datatables__: Creates the required datatables in a Postgres database to store insertion data from the Pipeline.
+ __learn__: Placeholder. Soon to have scikit-learn analysis.
+ __dashboard__: Generates the Dash dashboard. Contains simple queries for the database.

## Requirements
  + dash
  + psycopg2
  + pandas
  + plotly
  + json
  + requests

## Quickstart
1. Install the requirements
2. Add tables from __generate_datatables__ to a postgres db.
3. Add environment variables for RIOT_API_KEY, HOST (postgres location), USER (postgres username), and PASSWORD (postgres password)
4. Run `python pipeline PLAYERNAME PLAYERREGION TOTALPLAYERS` where PLAYERNAME is the name of player, PLAYERREGION is the players region (use NA1 for North American), and TOTALPLAYERS is how many players the alogorithm with branch out to to fill the database with 10 of their games.
5. Run `python dashboard`
6. Go to http://127.0.0.1:8050/

## Reference Material

Used Examples from Dash App Gallery for user interface examples and css [link](https://dash-gallery.plotly.host/Portal/)

League of Legends Analytics [Placeholder] isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
