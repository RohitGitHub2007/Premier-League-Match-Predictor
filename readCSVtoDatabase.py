import sqlite3
import pandas as pd

#Importing selected data from csv files

#creates/connects to the database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

#a cursor allows traversal of the database
cursor = connection.cursor()

#creates the table and columns with datatypes
cursor.execute("DROP TABLE IF EXISTS PremSeasonData")
cursor.execute("CREATE TABLE IF NOT EXISTS PremSeasonData ('Season' TEXT, 'Date' DATE, 'HomeTeam' TEXT, 'AwayTeam' TEXT, 'FTHG' INT, 'FTAG' INT, 'FTR' CHAR, 'B365H' DECIMAL(3, 2), 'B365D' DECIMAL(3, 2), 'B365A' DECIMAL(3, 2))")

seasons = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]


for i in range(len(seasons)):
    
    df = pd.read_csv(fr"C:\Users\rohit\Projects\Premier-League-Match-Predictor\Premier-League-CSVs\PL{seasons[i]}.csv", usecols=["Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","B365H","B365D","B365A"])
    df["Season"] = seasons[i]
    
    #puts the data into each database and commits
    #returns as an array
    dataRows = df.values.tolist()
    
    #returns as a tuple if you need this replace any subsequent 'dataRows' with 'dataToAdd'
    #dataToAdd = [(dRow[0], dRow[1], dRow[2], dRow[3], dRow[4], dRow[5], dRow[6], dRow[7], dRow[8]) for dRow in dataRows]
    
    #Debugging Test
    #print(df.columns)
    #print(len(dataRows[0]))
    #print(dataRows[0])
    #print(dataRows[0])
    
    cursor.executemany("INSERT INTO PremSeasonData ('Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A','Season') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataRows)
    connection.commit()

#close the connection
connection.close()