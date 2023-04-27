import pandas as pd
from tournament import Tournament

mapa = {'Champions': 8, '2ND' : 7, 'F4' : 6, 'E8' : 5, 'S16' : 4, 'R32' : 3, 'R64' : 2, 'R68' : 1}
df = pd.read_csv('./data/final/combined.csv')
df['POSTSEASON_value'] = df['POSTSEASON'].map(mapa)
df['QUALIFIED'] = ~pd.isna(df['SEED'])

def get_stat_difference(stat, team1, team2, year):
    team1_stat = df.loc[(df['School'] == team1) & (df['YEAR'] == year), stat].values[0]
    team2_stat = df.loc[(df['School'] == team2) & (df['YEAR'] == year), stat].values[0]
    return team1_stat - team2_stat


def make_training_data(tournaments, path):
    temp = {'Team1': [], 'Team2': [], 'Year': [], 'Team1Win': [],
     'SRS': [], 'ORB': [], 'PF': [], '3P': [], 'STL' : [], 'AST': [], 'BLK': [], 'FT%': [], 'TS%':[], 'SEED': []}
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
                                temp['STL'].append(get_stat_difference('STL', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['AST'].append(get_stat_difference('AST', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['BLK'].append(get_stat_difference('BLK', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['FT%'].append(get_stat_difference('FT%', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['TS%'].append(get_stat_difference('TS%', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
                                temp['SEED'].append(get_stat_difference('SEED', tournament.bracket[round][region][0], tournament.bracket[round][region][1], tournament.year))
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
                                temp['STL'].append(get_stat_difference('STL', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['AST'].append(get_stat_difference('AST', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['BLK'].append(get_stat_difference('BLK', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['FT%'].append(get_stat_difference('FT%', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['TS%'].append(get_stat_difference('TS%', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
                                temp['SEED'].append(get_stat_difference('SEED', tournament.bracket[round][region][1], tournament.bracket[round][region][0], tournament.year))
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
                                    temp['STL'].append(get_stat_difference('STL', matchup[0], matchup[1], tournament.year))
                                    temp['AST'].append(get_stat_difference('AST', matchup[0], matchup[1], tournament.year))
                                    temp['BLK'].append(get_stat_difference('BLK', matchup[0], matchup[1], tournament.year))
                                    temp['FT%'].append(get_stat_difference('FT%', matchup[0], matchup[1], tournament.year))
                                    temp['TS%'].append(get_stat_difference('TS%', matchup[0], matchup[1], tournament.year))
                                    temp['SEED'].append(get_stat_difference('SEED', matchup[0], matchup[1], tournament.year))
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
                                    temp['STL'].append(get_stat_difference('STL', matchup[1], matchup[0], tournament.year))
                                    temp['AST'].append(get_stat_difference('AST', matchup[1], matchup[0], tournament.year))
                                    temp['BLK'].append(get_stat_difference('BLK', matchup[1], matchup[0], tournament.year))
                                    temp['FT%'].append(get_stat_difference('FT%', matchup[1], matchup[0], tournament.year))
                                    temp['TS%'].append(get_stat_difference('TS%', matchup[1], matchup[0], tournament.year))
                                    temp['SEED'].append(get_stat_difference('SEED', matchup[1], matchup[0], tournament.year))
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
                    temp['STL'].append(get_stat_difference('STL', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['AST'].append(get_stat_difference('AST', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['BLK'].append(get_stat_difference('BLK', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['FT%'].append(get_stat_difference('FT%', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['TS%'].append(get_stat_difference('TS%', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
                    temp['SEED'].append(get_stat_difference('SEED', tournament.bracket[round][0], tournament.bracket[round][1], tournament.year))
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
                    temp['STL'].append(get_stat_difference('STL', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['AST'].append(get_stat_difference('AST', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['BLK'].append(get_stat_difference('BLK', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['FT%'].append(get_stat_difference('FT%', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['TS%'].append(get_stat_difference('TS%', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    temp['SEED'].append(get_stat_difference('SEED', tournament.bracket[round][1], tournament.bracket[round][0], tournament.year))
                    first = True

    data = pd.DataFrame(temp)
    data.to_csv(path, index=False)
               




YEAR_TEST = 2021
for j in range(2014,2024):
    if YEAR_TEST != 2020:
        tournaments = []
        for i in range(2014, 2024):
            if i not in [2020, YEAR_TEST]:
                tournament = Tournament(df, None, i)
                tournaments.append(tournament)

        make_training_data([Tournament(df, None, YEAR_TEST)], './data/model/testData.csv')
        make_training_data(tournaments, './data/model/trainingData.csv')

        