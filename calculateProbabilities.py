import sqlite3
import math
import pandas as pd
from calculateElo import teamsElo

#creates/connects to the database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

#a cursor allows traversal of the database
cursor = connection.cursor()

#creates the table and columns for TeamEloRatings which stores every teams elo rating on every date the played.
cursor.execute("DROP TABLE IF EXISTS PredictedOdds")
cursor.execute("CREATE TABLE IF NOT EXISTS PredictedOdds ('Season' TEXT, 'Date' DATE, 'HomeTeam' TEXT, 'AwayTeam' TEXT, 'FTHG' INT, 'FTAG' INT, 'FTR' CHAR, 'HomeOdds' DECIMAL(3, 2), 'DrawOdds' DECIMAL(3, 2), 'AwayOdds' DECIMAL(3, 2))")

#SQL statement to select from the PremSeasonData table
cursor.execute("SELECT Season, Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR FROM PremSeason20252026")

columnNames = ['Season', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HomeOdds', 'DrawOdds', 'AwayOdds']
df = pd.DataFrame(columns = columnNames)


scaleFactor = 400
homeAdvantage = 80
matches = 1
kfactor = 15
currentTeams = set()



#for Season, Date, HomeTeam, AwayTeam, fthg, ftag, ftr in cursor:
    
    