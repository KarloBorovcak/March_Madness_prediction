import pandas as pd
import numpy as np
from tournament import Tournament
from sklearn.linear_model import LogisticRegression

mapa = {'Champions': 8, '2ND' : 7, 'F4' : 6, 'E8' : 5, 'S16' : 4, 'R32' : 3, 'R64' : 2, 'R68' : 1}
df = pd.read_csv('./data/perGameStats/combined.csv')
df['POSTSEASON_value'] = df['POSTSEASON'].map(mapa)
df['QUALIFIED'] = ~pd.isna(df['SEED'])

def get_stat_difference(stat, team1, team2, year):
    team1_stat = df.loc[(df['School'] == team1) & (df['YEAR'] == year), stat].values[0]
    team2_stat = df.loc[(df['School'] == team2) & (df['YEAR'] == year), stat].values[0]
    return team1_stat - team2_stat


def make_training_data(tournaments, path):
    temp = {'Team1': [], 'Team2': [], 'Year': [], 'Team1Win': [], 'SRS': [], 'ORB': [], 'PF': [], '3P': []}
    first = True
    for tournament in tournaments:
        for round in tournament.bracket.keys():
            if round != 'Champions':
                for region in tournament.bracket[round]:   
                        if tournament.bracket[round][region] == []:
                            continue
                        if round == 'F4':
                            if first:
                                temp['Team1'].append(tournament.bracket[round][region][0])
                                temp['Team2'].append(tournament.bracket[round][region][1])
                                temp['Team1Win'].append(1)
                                temp['Year'].append(tournament.year)
                                temp['SRS'].append(get_stat_difference('SRS', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['ORB'].append(get_stat_difference('ORB', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['PF'].append(get_stat_difference('PF', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['3P'].append(get_stat_difference('3P', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                first = False
                            else:
                                temp['Team1'].append(tournament.bracket[round][region][1])
                                temp['Team2'].append(tournament.bracket[round][region][0])
                                temp['Team1Win'].append(0)
                                temp['Year'].append(tournament.year)
                                temp['SRS'].append(get_stat_difference('SRS', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['ORB'].append(get_stat_difference('ORB', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['PF'].append(get_stat_difference('PF', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['3P'].append(get_stat_difference('3P', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                first = True
                        else:
                            for matchup in tournament.bracket[round][region]:
                                if first:
                                    temp['Team1'].append(matchup[0])
                                    temp['Team2'].append(matchup[1])
                                    temp['Team1Win'].append(1)
                                    temp['Year'].append(tournament.year)
                                    temp['SRS'].append(get_stat_difference('SRS', matchup[0], matchup[1], tournament.year))
                                    temp['ORB'].append(get_stat_difference('ORB', matchup[0], matchup[1], tournament.year))
                                    temp['PF'].append(get_stat_difference('PF', matchup[0], matchup[1], tournament.year))
                                    temp['3P'].append(get_stat_difference('3P', matchup[0], matchup[1], tournament.year))
                                    first = False
                                else:
                                    temp['Team1'].append(matchup[1])
                                    temp['Team2'].append(matchup[0])
                                    temp['Team1Win'].append(0)
                                    temp['Year'].append(tournament.year)
                                    temp['SRS'].append(get_stat_difference('SRS', matchup[1], matchup[0], tournament.year))
                                    temp['ORB'].append(get_stat_difference('ORB', matchup[1], matchup[0], tournament.year))
                                    temp['PF'].append(get_stat_difference('PF', matchup[1], matchup[0], tournament.year))
                                    temp['3P'].append(get_stat_difference('3P', matchup[1], matchup[0], tournament.year))
                                    first = True
            else:
                if first:
                    temp['Team1'].append(tournament.bracket[round][0])
                    temp['Team2'].append(tournament.bracket[round][1])
                    temp['Team1Win'].append(1)
                    temp['Year'].append(tournament.year)
                    temp['SRS'].append(get_stat_difference('SRS', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['ORB'].append(get_stat_difference('ORB', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['PF'].append(get_stat_difference('PF', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['3P'].append(get_stat_difference('3P', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    first = False
                else:
                    temp['Team1'].append(tournament.bracket[round][1])
                    temp['Team2'].append(tournament.bracket[round][0])
                    temp['Team1Win'].append(0)
                    temp['Year'].append(tournament.year)
                    temp['SRS'].append(get_stat_difference('SRS', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['ORB'].append(get_stat_difference('ORB', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['PF'].append(get_stat_difference('PF', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['3P'].append(get_stat_difference('3P', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    first = True

    data = pd.DataFrame(temp)
    data.to_csv(path, index=False)

def make_test_data(tournament):
    temp = {'Team1': [], 'Team2': [], 'Team1Win': [], 'Year': []}
    for round in tournament.bracket.keys():
            if round != 'Champions':
                for region in tournament.bracket[round]:   
                        if tournament.bracket[round][region] == []:
                            continue
                        if round == 'F4':
                            if first:
                                temp['Team1'].append(tournament.bracket[round][region][0])
                                temp['Team2'].append(tournament.bracket[round][region][1])
                                temp['Team1Win'].append(1)
                                temp['Year'].append(tournament.year)
                                first = False
                            else:
                                temp['Team1'].append(tournament.bracket[round][region][1])
                                temp['Team2'].append(tournament.bracket[round][region][0])
                                temp['Team1Win'].append(0)
                                temp['Year'].append(tournament.year)
                                first = True
                            
                        else:
                            for matchup in tournament.bracket[round][region]:
                                if first:
                                    temp['Team1'].append(matchup[0])
                                    temp['Team2'].append(matchup[1])
                                    temp['Team1Win'].append(1)
                                    temp['Year'].append(tournament.year)
                                    first = False
                                else:
                                    temp['Team1'].append(matchup[1])
                                    temp['Team2'].append(matchup[0])
                                    temp['Team1Win'].append(0)
                                    temp['Year'].append(tournament.year)
                                    first = True
                                
            else:
                if first:
                    temp['Team1'].append(tournament.bracket[round][0])
                    temp['Team2'].append(tournament.bracket[round][1])
                    temp['Team1Win'].append(1)
                    temp['Year'].append(tournament.year)
                    first = False
                else:
                    temp['Team1'].append(tournament.bracket[round][1])
                    temp['Team2'].append(tournament.bracket[round][0])
                    temp['Team1Win'].append(0)
                    temp['Year'].append(tournament.year)
                    first = True
               





tournaments = []

for i in range(2014, 2022):
    if i not in [2020, 2019, 2021]:
        tournament = Tournament(df, None, i)
        tournaments.append(tournament)

make_training_data([Tournament(df, None, 2019), Tournament(df, None, 2021)], './data/model/testData.csv')
make_training_data(tournaments, './data/model/trainingData.csv')

dftrain = pd.read_csv('./data/model/trainingData.csv')
dftest = pd.read_csv('./data/model/testData.csv')

model = LogisticRegression(random_state=0).fit(dftrain[['SRS', 'ORB', 'PF', '3P']], dftrain['Team1Win'])

prediction = model.predict(dftest[['SRS', 'ORB', 'PF', '3P']])
dftest['Prediction'] = prediction
dftest.to_csv('./data/model/predictions.csv', index=False)
print(model.score(dftest[['SRS', 'ORB', 'PF', '3P']], dftest['Team1Win']))
# print('--------------------------------')
# print(np.where(dftest['Prediction'] == dftest['Team1Win'], 1, 0).sum() / len(dftest['Prediction']))
