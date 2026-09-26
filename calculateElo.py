import sqlite3

#creates/connects to the database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

#a cursor allows traversal of the database
cursor = connection.cursor()

#creates the table and columns with datatypes
cursor.execute("DROP TABLE IF EXISTS TeamEloRatings")
cursor.execute("CREATE TABLE IF NOT EXISTS TeamEloRatings ('Season' TEXT, 'Date' DATE, 'Team' TEXT, 'Elo' FLOAT)")

#SQL statement to select from the PremSeasonData table
cursor.execute("SELECT Season, Date, HomeTeam, AwayTeam, FTR FROM PremSeasonData")

homeAdvantage = 0

for Season, Date, HomeTeam, AwayTeam, ftr in cursor:
    print(Season, Date, HomeTeam, AwayTeam, ftr)
    
    cursor.execute("INSERT")
    
connection.close()