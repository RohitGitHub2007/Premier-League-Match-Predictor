import sqlite3
import pandas as pd
import math

#creates/connects to the database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

cursor1 = connection.cursor()
cursor2 = connection.cursor()
cursor3 = connection.cursor()
cursor4 = connection.cursor()

cursor1.execute("SELECT Season, Date, HomeTeam, AwayTeam, HomeProbability, DrawProbability, AwayProbability, FTR FROM PredictedProbabilities")
cursor2.execute("SELECT Season, Date, HomeTeam, AwayTeam, B365H, B365D, B365A, FTR FROM PremSeason20252026")
cursor3.execute("SELECT Season, Date, HomeTeam, AwayTeam, HomeProbability, DrawProbability, AwayProbability, FTR FROM PredictedProbabilities")
cursor4.execute("SELECT Season, Date, HomeTeam, AwayTeam, HomeProbability, DrawProbability, AwayProbability, FTR FROM PredictedProbabilities")

#variable holds the brier score
totalBrierScore = 0
baseTotalBrierScore = 0
bet365TotalBrierScore = 0
frequencyTotalBrierScore = 0
length = 0
baseLength = 0
bet365Length = 0
frequencyLength = 0


#loop to calculate a baseline score assuming the chance of each outcome being equal
for Season, Date, HomeTeam, AwayTeam, HomeProbability, DrawProbability, AwayProbability, ftr in cursor3:
    
    baseLength += 1
    
    if ftr == 'A': 
        baseBrierScore = pow((1/3 - 1), 2) + pow((1/3 - 0), 2) + pow((1/3 - 0), 2)
    elif ftr == 'D':
        baseBrierScore = pow((1/3 - 0), 2) + pow((1/3 - 1), 2) + pow((1/3 - 0), 2)
    elif ftr == 'H':
        baseBrierScore = pow((1/3 - 0), 2) + pow((1/3 - 0), 2) + pow((1/3 - 1), 2)
        
    baseTotalBrierScore = baseTotalBrierScore + baseBrierScore
    
    
baseAvgBrierScore = baseTotalBrierScore/(baseLength)

print(baseAvgBrierScore)

#loop to calculate a frequency baseline score using the frequency of each result from the historic data (PremSeasonData Table)
for Season, Date, HomeTeam, AwayTeam, HomeProbability, DrawProbability, AwayProbability, ftr in cursor4:
    
    frequencyLength += 1
    
    if ftr == 'A': 
        frequencyBrierScore = pow((1297/4370 - 1), 2) + pow((429/1748 - 0), 2) + pow((4001/8740 - 0), 2)
    elif ftr == 'D':
        frequencyBrierScore = pow((1297/4370 - 0), 2) + pow((429/1748 - 1), 2) + pow((4001/8740 - 0), 2)
    elif ftr == 'H':
        frequencyBrierScore = pow((1297/4370 - 0), 2) + pow((429/1748 - 0), 2) + pow((4001/8740 - 1), 2)
        
    frequencyTotalBrierScore = frequencyTotalBrierScore + frequencyBrierScore
    
    
frequencyAvgBrierScore = frequencyTotalBrierScore/(frequencyLength)

print(frequencyAvgBrierScore)

#loops through the predicted probabilities for each match then totals and calculates the average
for Season, Date, HomeTeam, AwayTeam, HomeProbability, DrawProbability, AwayProbability, ftr in cursor1:
    
    length += 1
    
    if ftr == 'A': 
        brierScore = pow((AwayProbability - 1), 2) + pow((DrawProbability - 0), 2) + pow((HomeProbability - 0), 2)
    elif ftr == 'D':
        brierScore = pow((AwayProbability - 0), 2) + pow((DrawProbability - 1), 2) + pow((HomeProbability - 0), 2)
    elif ftr == 'H':
        brierScore = pow((AwayProbability - 0), 2) + pow((DrawProbability - 0), 2) + pow((HomeProbability - 1), 2)
        
    totalBrierScore = totalBrierScore + brierScore
    
    
avgBrierScore = totalBrierScore/(length)

print(avgBrierScore)

#loops through the actual bookmaker odds to find the brier score for Bet365
for Season, Date, HomeTeam, AwayTeam, b365H, b365D, b365A, ftr in cursor2:
    
    bet365Length += 1
    
    tempA = 1/b365A
    tempD = 1/b365D
    tempH = 1/b365H
    
    totalProbability = tempA + tempD + tempH
    
    AwayProbability = tempA/totalProbability
    DrawProbability = tempD/totalProbability
    HomeProbability = tempH/totalProbability
    
    
    
    if ftr == 'A':  
        bet365BrierScore = pow((AwayProbability - 1), 2) + pow((DrawProbability - 0), 2) + pow((HomeProbability - 0), 2)
    elif ftr == 'D':
        bet365BrierScore = pow((AwayProbability - 0), 2) + pow((DrawProbability - 1), 2) + pow((HomeProbability - 0), 2)
    elif ftr == 'H':
        bet365BrierScore = pow((AwayProbability - 0), 2) + pow((DrawProbability - 0), 2) + pow((HomeProbability - 1), 2)
        
    bet365TotalBrierScore = bet365TotalBrierScore + bet365BrierScore
    
    
bet365AvgBrierScore = bet365TotalBrierScore/(bet365Length)

print(bet365AvgBrierScore)