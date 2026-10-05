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

## 27/09/2026

Implemented elo formula to calculate expected elo rating and elo rating after the match. Also implemented code to create a table called teamEloRatings which stores every elo update for every team across every season. This way we can see how a teams' elo rating changes thoughout each season.

Decided to use a hashMap called teamsElo to store each team and their elo rating. This way elos for specific teams can be preserved as they get relegated and promoted. Newly promoted teams still start with a base elo rating of 1500. This will have to be remedied as it is expected for a newly promoted team to have a lower elo rating than average.

Used eloratings.net/about to find a way to implement victoryMarginMultiplier (K factor). K factor affects how much a single match moves a rating. In this system goal difference also affects how much the match moves the rating.

Used a k factor of 15 to ensure ratings were affected more by recent results but not too high of a value such that elo was influenced heavily by a short run of good form or lucky wins for each team.

Considering using more csv files of older premier league seasons the create more accurate predictions and elo ratings.

## 29/09/2026

Decided to add previous seasons to create a more accurate model/prediction starting from the 2002-03 season. (Specifically chose this as it was when data on B365 odds started to be stored).

Added in a temporary resolution to the promoted teams' starting elo. When they enter the league they start with 1350 elo(roughly what a relegated teams' elo sits at). However this method is not perfect and with change the total sum of the leagues Elo ratings. Will have to remedy this later by adjusting every team in that current seasons' rating slightly.

## 01/10/2026

Implemented loader for the test season csv and have started on the file responsible for calculating probabilites

Decided the draw probability should be decided based on the rating gap between the two teams.
Another option considered was a constant draw rate. This idea was rejected because it doesn't simulate the fact that teams with a bigger rating gap are less likely to draw in real life and vice versa.

This would need pre-match ratings which arent stored in a database as of now, so that would need to be implemented into the pipeline at the moment the pre-match ratings are calculated.

Currently leaning towards keeping calculations as probabilities and then converting the bookmaker odds into probabilities for comparison.

## 02/10/2026

Decided upon using a logistic regression model to decide win, draw and loss probabilities. This involves creating a python script that look at all the historic data (mainly elo differences before games and what the outcomes of these games were) and then find three values.

The first value is the beta which usually takes the form of a tiny decimal number. This measures how much the pre-match rating gap matters in the league.

The second is the loss/draw boundary. A match on this boundary has a 50% chance of an away win and the further left of it a match is, the higher that chance.

The third is the draw/win boundary. A match on this boundary has a 50% chance of a home win and the further right of it a match is, the higher that chance. A match between the two boundaries has a higher chance of a draw than a match outside them.

Implemented a python script to get all three of the above values. Used statsmodels library for the ordered logistic regression model. The model was fitted on historic premier league data from 2002/2003 to 2024/2025.

Implemented probability formulas in calculateProbabilities.py and stored the data into the PredictedProbabilities table.

Ran an AVG() function on the PredictedProbabilities table and found that the predicted average Draw Probability was 0.248(24.8%) when comparing this to various actual league statistic websites online it was found that the draw rate for that season was 0.273(27.3%) which shows that the model is calibrated.

## 04/10/2026

Implemented the Brier score calculator. Used a baseline score (probability of each outcome was divided equally), a score based on the frequency of each outcome from previous seasons, a score based on the current elo prediction system and a score based on bet365 odds (converted into probabilities). Due to the bookmakers adding an overround (extra profit margins added by bookmakers so that the house wins in the long term) the regular 1/odds values were not usable and so to get the probability (which sums to 1), each value was divided by the total combined value for the three skewed probabilities to normalize them.

From the results it is determined that the system outperforms the equal probability baseline and the frequency baseline. Although the score was close to that of bet365's it was slightly worse. This may be due to bookmakers taking into account more advanced data such as player injuries, xG, xA etc.

It was decided that tuning to the system should be stopped after the brier score for the 2025/26 season was calculated, this was to avoid purposely changing the system to lower the brier score. Doing this would make it more accurate for the specific test season but it may not be what applies best to future seasons.

Some remaining weak spots in the system:

The promoted and relegated teams do not cleanly exchange elo and so the total elo for all the teams combined slightly varies from season to season.

The k-factor, home advantage and starting elo were all picked based on what was commonly used online and suggested for a project like this. They are not as specific to this system as they could be.

There is only one test season, we don't know how this system compares to the bookmakers in future seasons and if the model itself is consistently accurate for multiple seasons or only the specific test season. More seasons can be tested in the future.
