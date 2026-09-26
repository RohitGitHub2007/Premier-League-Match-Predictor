# NOTES LOG

## 23/09/2026

Needed to convert the DD/MM/YYYY to ISO format for sorting etc on SQLite.

Decided to exclude time and other stats that don't serve a purpose for elo calculation or bookmakers comparisons.

Initially wanted to make 5 separate tables to store each season's csv file but then reasoned that it would be better to have all the csv's in one file for elo calculation and have a season column which keeps queries per season possible using GROUP BY.

Drop and rebuild during development, switch to insert or ignore once loading is incremental.

Any values go through '?' placeholders, not string formatting. SQLite would have treated an unquoted 2020-21 as arithmetic and stored it as 1999. '?' tells the database to use the datatype that the program gave it.

With string formatting a user could type something that closes the quote and then add in their own SQL like 'DROP TABLE'. This is called an SQL Injection. Paramterised queries are the common way to defend against things like this happening.

The column list existed in three places, usecols, the row building line and the insert statement. This means that changes have to be made in all three places to work. This was fixed by deleting a line of code that converted the array into tuples which added nothing and also built 9 columns instead of 10.

In the future code should be used that takes the shape of the data from the original piece of data e.g len(seasons) instead of range(5).

## 24/09/2026

Used SQL queries in DB browser to verify if the csv loader worked correctly. Compared Away and Home win records for Chelsea over each season to online databases e.g FOTMOB.

## 26/09/2026

Created the calculateElo.py file. Implemented setup for a new table called TeamEloRatings to store each teams elo on a particular date after a game. 

Made a loop to loop through every entry in the PremSeasonData table adn calculate elo up to that entry as well as add it to the TeamELoRating table to preserve the history of each team's elo rating and how it changed over the seasons.

Need to decide how to handle relegated and promoted teams' elo rating tommorrow.
