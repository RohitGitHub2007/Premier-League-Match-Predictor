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

seasons = ["2002-03", "2003-04", "2004-05", "2005-06", "2006-07",
           "2007-08", "2008-09", "2009-10", "2010-11", "2011-12",
           "2012-13", "2013-14", "2014-15", "2015-16", "2016-17",
           "2017-18", "2018-19", "2019-20", "2020-21", "2021-22",
           "2022-23", "2023-24", "2024-25"]


for i in range(len(seasons)):
    
    #reads the csv, some of the older files contain character saved in an older format 
    # - "Windows-1252" while pandas tries to use UTF-8 decoder by default. So we set
    # decoder explicitly.
    
    df = pd.read_csv(fr"C:\Users\rohit\Projects\Premier-League-Match-Predictor\Premier-League-CSVs\PL{seasons[i]}.csv", usecols=["Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","B365H","B365D","B365A"], encoding = "windows-1252")
    df["Season"] = seasons[i]
    
    #Changes date to ISO format (format = "mixed" allows pandas to switch between %Y and %y layout as seen in the csv)
    df["Date"] = (pd.to_datetime(df["Date"], format = "mixed", dayfirst = True, errors = 'coerce')).dt.strftime(r"%Y-%m-%d")
    
    
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