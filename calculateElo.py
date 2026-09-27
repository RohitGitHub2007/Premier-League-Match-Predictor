import sqlite3
import math
import pandas as pd

#creates/connects to the database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

#a cursor allows traversal of the database
cursor = connection.cursor()

#creates the table and columns for TeamEloRatings which stores every teams elo rating on every date the played.
cursor.execute("DROP TABLE IF EXISTS TeamEloRatings")
cursor.execute("CREATE TABLE IF NOT EXISTS TeamEloRatings ('Season' TEXT, 'Date' DATE, 'Team' TEXT, 'Elo' FLOAT)")

#SQL statement to select from the PremSeasonData table
cursor.execute("SELECT Season, Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR FROM PremSeasonData")

#inititalizing variables, hashMaps
teamsElo  = {}
scaleFactor = 400
homeAdvantage = 400
matches = 1
kfactor = 15

#initializing dataframe for TeamEloRatings
columnNames = ['Season', 'Date', 'Team', 'Elo']
df = pd.DataFrame(columns = columnNames)



#decayRate influences how quickly older matches are forgotten (0.1 = very quickly, 0.01 = very slowly)
decayRate = 0.693



for Season, Date, HomeTeam, AwayTeam, fthg, ftag, ftr in cursor:
    
    
    #adds teams that arent already in the hashMap and assign them a default rating of 1500
    if HomeTeam not in teamsElo:
        teamsElo[HomeTeam] = 1500
        
    if AwayTeam not in teamsElo:
        teamsElo[AwayTeam] = 1500
        
    victoryMargin = abs(fthg - ftag)
    
    #calculate the multiplier for each result based on the goal difference of the match (k factor)
    if victoryMargin >= 4:
        victoryMarginMultiplier = kfactor*(1 + (3/4 + ((victoryMargin - 3)/8)))
    elif victoryMargin == 3:
        victoryMarginMultiplier = kfactor*(1 + 3/4)
    elif victoryMargin == 2:
        victoryMarginMultiplier = kfactor*(1 + 0.5)
    else:
        victoryMarginMultiplier = kfactor*(1)
        
    effectiveVictoryMarginMultiplier = victoryMarginMultiplier #* pow(math.e, -(decayRate * matches))
    
    
       
    #expected elo ratings before the match
    expectedEloHome = 1 / (1 + pow(10,(teamsElo[AwayTeam] - (teamsElo[HomeTeam] + homeAdvantage))/scaleFactor))
    expectedEloAway =  1 - expectedEloHome
    
    if ftr == "A":
        resultH = 0
        resultA = 1
    elif ftr == "H":
        resultH = 1
        resultA = 0
    elif ftr == "D":
        resultH = 0.5
        resultA = 0.5
    
    #elo rating updates after the match
    teamsElo[HomeTeam] = teamsElo[HomeTeam] + (effectiveVictoryMarginMultiplier * (resultH - expectedEloHome))
    teamsElo[AwayTeam] = teamsElo[AwayTeam] + (effectiveVictoryMarginMultiplier * (resultA - expectedEloAway))
    
    #countes number of matches since model started. Helps weight recent matches more than previous matches.
    matches += 1
    
    df.loc[len(df)] = [Season, Date, HomeTeam, teamsElo[HomeTeam]]
    df.loc[len(df)] = [Season, Date, AwayTeam, teamsElo[AwayTeam]]
    
    
    #debugging print statements
    #print(Season, Date, HomeTeam, AwayTeam, ftr,)
    #print((HomeTeam, teamsElo[HomeTeam]), (AwayTeam, teamsElo[AwayTeam]))
    #print(victoryMargin)
    
    #cursor.execute("INSERT")
    
#insert data from the dataframe in TeamEloRatings table    
dataRows = df.values.tolist()
cursor.executemany("INSERT INTO TeamEloRatings ('Season', 'Date', 'Team', 'Elo') VALUES (?, ?, ?, ?)", dataRows)
connection.commit()
    
connection.close()