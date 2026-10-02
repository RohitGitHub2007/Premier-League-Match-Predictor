import sqlite3
import pandas as pd
import numpy as np
from statsmodels.miscmodels.ordinal_model import OrderedModel

#connects to sqlite database
connection = sqlite3.connect(r'C:\Users\rohit\Projects\Premier-League-Match-Predictor\PremierLeagueDatabase.db')

cursor = connection.cursor()

cursor.execute("SELECT EloDifference, MatchOutcome FROM EloDifferenceAndOutcome")

#create dataframe to store data from the database
columnNames = ['EloDifference', 'MatchOutcome']
df = pd.DataFrame(columns = columnNames)

for EloDifference, MatchOutcome in cursor:
    df.loc[len(df)] = [EloDifference, MatchOutcome]
    
df['MatchOutcome'] = pd.Categorical(df['MatchOutcome'], categories = [0,1,2], ordered = True)

#test to make sure database loaded correctly   
#print(df)

#initializing model
model = OrderedModel(df['MatchOutcome'], df['EloDifference'], offset = None, distr = 'logit')
#analyzes historical data, finds statistical patterns then locks in beta, loss/draw cut and draw/win cut
results = model.fit()

#print summary of results
print(results.summary())

#prints the clean results for the cutoffs
print(model.transform_threshold_params(results.params[1:]))

#from results
#beta = 0.0050
#loss/draw(0/1) cutoff = -0.9909
#draw/win(1/2) cutoff = 0.1780

