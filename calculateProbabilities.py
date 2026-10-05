import sqlite3
import math
import pandas as pd

#creates/connects to the database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

#a cursor allows traversal of the database
cursor = connection.cursor()

#creates the table and columns for TeamEloRatings which stores every teams elo rating on every date the played.
cursor.execute("DROP TABLE IF EXISTS PredictedProbabilities")
cursor.execute("CREATE TABLE IF NOT EXISTS PredictedProbabilities ('Season' TEXT, 'Date' DATE, 'HomeTeam' TEXT, 'AwayTeam' TEXT, 'HomeProbability' DECIMAL(3, 2), 'DrawProbability' DECIMAL(3, 2), 'AwayProbability' DECIMAL(3, 2), 'FTR' CHAR)")

#store each teams elo rating before the latest season in a hashMap
cursor.execute("SELECT Team, Elo FROM TeamEloRatings")
teamsElo = {}

for Team, Elo in cursor:
    teamsElo[Team] = Elo


#SQL statement to select from the PremSeasonData table
cursor.execute("SELECT Season, Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR FROM PremSeason20252026")

columnNames = ['Season', 'Date', 'HomeTeam', 'AwayTeam', 'HomeProbability', 'DrawProbability', 'AwayProbability', 'FTR']
df = pd.DataFrame(columns = columnNames)


scaleFactor = 400
homeAdvantage = 80
matches = 1
kfactor = 15
currentTeams = set()
beta = 0.0050
cutoff1 = -0.9909
cutoff2 = 0.2039



for Season, Date, HomeTeam, AwayTeam, fthg, ftag, ftr in cursor:
    
    #skips if any of these fields are null (means game was cancelled)
    if HomeTeam is None or AwayTeam is None:
        continue
    
    if fthg is None or ftag is None:
        continue
    
    
    #adds teams that arent already in the hashMap and assigns them a default rating of 1350
    #unless the teams were in the original 20 they start off with a league average of 1500
    if HomeTeam not in teamsElo:
       teamsElo[HomeTeam] = 1350
        
    if AwayTeam not in teamsElo:
        teamsElo[AwayTeam] = 1350
       
              
    #decides result for elo calculation and also decides match outcome for home team
    if ftr == "A":
        resultH = 0
        resultA = 1
        matchOutcome = 0
        
    elif ftr == "H":
        resultH = 1
        resultA = 0
        matchOutcome = 2
    
    elif ftr == "D":
        resultH = 0.5
        resultA = 0.5
        matchOutcome = 1
        
    #calculate pre-match elo difference for home team    
    preMatchEloDifference = teamsElo[HomeTeam] - teamsElo[AwayTeam]
    
    
    #----------------------------------------------------------------------------------------------------------
    #This code is for calculating the probabilities for the 2025-26 Season (the season has passed
    # but we are assuming it hasn't for these calculations, we will then compare our results to the actual
    # bookmaker odds later)
    
    #match position (scales the teams gap onto the models timeline)
    
    matchPosition = preMatchEloDifference * beta
    
    awayWin = cutoff1 - matchPosition
    awayWinProb = 1/(1 + (pow(math.e, (-1 * awayWin))))
    
    awayWinAndDraw = cutoff2 - matchPosition
    awayWinAndDrawProb = 1/(1 + (pow(math.e, (-1 * awayWinAndDraw))))
    
    drawProb = awayWinAndDrawProb - awayWinProb
    
    homeWinProb = 1 - awayWinAndDrawProb
    
    
    df.loc[len(df)] = [Season, Date, HomeTeam, AwayTeam, homeWinProb, drawProb, awayWinProb, ftr]
    
    
    #----------------------------------------------------------------------------------------------------------    
    
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
        
    effectiveVictoryMarginMultiplier = victoryMarginMultiplier 
    
    
        
    #expected elo ratings before the match
    expectedEloHome = 1 / (1 + pow(10,(teamsElo[AwayTeam] - (teamsElo[HomeTeam] + homeAdvantage))/scaleFactor))
    expectedEloAway =  1 - expectedEloHome
    
    
        
    prevRatingH = teamsElo[HomeTeam]
    prevRatingA = teamsElo[AwayTeam]
    
    #elo rating updates after the match
    teamsElo[HomeTeam] = teamsElo[HomeTeam] + (effectiveVictoryMarginMultiplier * (resultH - expectedEloHome))
    teamsElo[AwayTeam] = teamsElo[AwayTeam] + (effectiveVictoryMarginMultiplier * (resultA - expectedEloAway))
    
    changeH = abs(teamsElo[HomeTeam] - prevRatingH)
    changeA = abs(teamsElo[AwayTeam] - prevRatingA)
    
dataRows = df.values.tolist()
cursor.executemany("INSERT INTO PredictedProbabilities ('Season', 'Date', 'HomeTeam', 'AwayTeam', 'HomeProbability', 'DrawProbability', 'AwayProbability', 'FTR') VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dataRows)
connection.commit()

connection.close()