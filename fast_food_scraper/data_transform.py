import pandas as pd

df = pd.read_csv('data/census_parlimen.csv')
df = df.filter(['state', 'Parliament_Seat'])
#print(parliament_constituency.head())
#state_list = parliament_constituency['state'].to_dict()
mydict = {}
for state, area in df.groupby('state'):
    mydict.update({state: area["Parliament_Seat"].to_list()})

print(mydict)
