import pandas as pd
from tournament import Tournament



mapa = {'Champions': 8, '2ND' : 7, 'F4' : 6, 'E8' : 5, 'S16' : 4, 'R32' : 3, 'R64' : 2, 'R68' : 1}

df = pd.read_csv('./data/perGameStats/combined.csv')
df['POSTSEASON_value'] = df['POSTSEASON'].map(mapa)
df['QUALIFIED'] = ~pd.isna(df['SEED'])



tournament = Tournament(df, None, 2021)
print(tournament.bracket)
print('------------------------------------')
tournament.predict_bracket()