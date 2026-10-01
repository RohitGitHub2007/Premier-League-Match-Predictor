import sqlite3
import math
import pandas as pd



#Importing selected data from 2025-26 Season

#creates/connects to the database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

#a cursor allows traversal of the database
cursor = connection.cursor()

#creates the table and columns with datatypes
cursor.execute("DROP TABLE IF EXISTS PremSeason20252026")
cursor.execute("CREATE TABLE IF NOT EXISTS PremSeason20252026 ('Season' TEXT, 'Date' DATE, 'HomeTeam' TEXT, 'AwayTeam' TEXT, 'FTHG' INT, 'FTAG' INT, 'FTR' CHAR, 'B365H' DECIMAL(3, 2), 'B365D' DECIMAL(3, 2), 'B365A' DECIMAL(3, 2))")
    
#reads the csv, some of the older files contain character saved in an older format 
# - "Windows-1252" while pandas tries to use UTF-8 decoder by default. So we set
# decoder explicitly.
    
df = pd.read_csv(fr"C:\Users\rohit\Projects\Premier-League-Match-Predictor\Premier-League-CSVs\PL2025-26.csv", usecols=["Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","B365H","B365D","B365A"], encoding = "windows-1252")
df["Season"] = "2025-26"
    
#Changes date to ISO format (format = "mixed" allows pandas to switch between %Y and %y layout as seen in the csv)
df["Date"] = (pd.to_datetime(df["Date"], format = "mixed", dayfirst = True, errors = 'coerce')).dt.strftime(r"%Y-%m-%d")
    
    
#puts the data into each database and commits
#returns as an array
dataRows = df.values.tolist()
    
#returns as a tuple if you need this replace any subsequent 'dataRows' with 'dataToAdd'
#dataToAdd = [(dRow[0], dRow[1], dRow[2], dRow[3], dRow[4], dRow[5], dRow[6], dRow[7], dRow[8]) for dRow in dataRows]

cursor.executemany("INSERT INTO PremSeason20252026 ('Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A','Season') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataRows)
connection.commit()

#close the connection
connection.close()