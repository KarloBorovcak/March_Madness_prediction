import pandas as pd

regions = ['EAST', 'MIDWEST', 'SOUTH', 'WEST']
final_four = {'2021':['SOUTH', 'MIDWEST'], '2019':['SOUTH','MIDWEST'], '2018':['SOUTH','EAST'], 
'2017':['SOUTH','MIDWEST'], '2016':['SOUTH','WEST'], '2015':['SOUTH','EAST'], '2014':['SOUTH','EAST']}

rounds = ['R68', 'R64', 'R32', 'S16', 'E8', 'F4', 'Champions']

class Tournament:
    def __init__(self, dataset, model, year):
        self.df = dataset.loc[dataset['YEAR'] == year]
        self.year = year
        self.model = model
        self.bracket = self.generate_bracket()

    def generate_bracket(self):
        generated = {}
        for j,round in enumerate(rounds):
            if round == 'R68':
                r68 = {}
                for region in regions:
                    temp = []
                    for team in self.df.loc[(self.df['REGION'] == region) & (self.df['POSTSEASON'] == 'R68')]['School']:
                        teams = [self.df.loc[(self.df['REGION'] == region) & (self.df['POSTSEASON'] != round ) & (self.df["SEED"] == self.df.loc[self.df["School"] == team].SEED.values[0])]['School'].values[0], team]
                        temp.append(teams)
                    r68[region] = temp
                generated[round] = r68
            
            elif round == 'R64':
                r64 = {}
                for region in regions:
                    temp = []
                    tempdf = self.df.loc[(self.df['REGION'] == region) & (self.df['POSTSEASON'] != 'R68')]
                    tempdf.sort_values(by=['SEED'], inplace=True)
                    lista = list(tempdf['School'])
                    temp.append([lista[15], lista[0]] if self.df.loc[(self.df["School"] == lista[0])]["POSTSEASON"].values[0] == 'R64' else [lista[0], lista[15]])
                    temp.append([lista[8], lista[7]] if self.df.loc[(self.df["School"] == lista[7])]["POSTSEASON"].values[0] == 'R64' else [lista[7], lista[8]])
                    temp.append([lista[11], lista[4]] if self.df.loc[(self.df["School"] == lista[4])]["POSTSEASON"].values[0] == 'R64' else [lista[4], lista[11]])
                    temp.append([lista[12], lista[3]] if self.df.loc[(self.df["School"] == lista[3])]["POSTSEASON"].values[0] == 'R64' else [lista[3], lista[12]])
                    temp.append([lista[10], lista[5]] if self.df.loc[(self.df["School"] == lista[5])]["POSTSEASON"].values[0] == 'R64' else [lista[5], lista[10]])
                    temp.append([lista[13], lista[2]] if self.df.loc[(self.df["School"] == lista[2])]["POSTSEASON"].values[0] == 'R64' else [lista[2], lista[13]])
                    temp.append([lista[9], lista[6]] if self.df.loc[(self.df["School"] == lista[6])]["POSTSEASON"].values[0] == 'R64' else [lista[6], lista[9]])
                    temp.append([lista[14], lista[1]] if self.df.loc[(self.df["School"] == lista[1])]["POSTSEASON"].values[0] == 'R64' else [lista[1], lista[14]])
                    r64[region] = temp
                generated[round] = r64

            elif round =='F4':
                f4 = {}
                lista = []
                for region in regions:
                    lista.append(generated[rounds[j-1]][region][0])

                matchup1 = final_four[str(self.year)]
                matchup2 = list(set(regions) - set(matchup1))

                match1 = [lista[regions.index(matchup1[0])], lista[regions.index(matchup1[1])]]
                match2 = [lista[regions.index(matchup2[0])], lista[regions.index(matchup2[1])]]

                f4['-'.join(matchup1)] = [match1[0][0], match1[1][0]] if self.df.loc[(self.df["School"] == match1[1][0])]["POSTSEASON"].values[0] == 'F4' else [match1[1][0], match1[0][0]]
                f4['-'.join(matchup2)] = [match2[0][0], match2[1][0]] if self.df.loc[(self.df["School"] == match2[1][0])]["POSTSEASON"].values[0] == 'F4' else [match2[1][0], match2[0][0]]

                generated[round] = f4

            elif round == 'Champions':
                lista = []
                for region in generated[rounds[j-1]].keys():
                    lista.append(generated[rounds[j-1]][region][0])

                generated[round]  = [lista[0], lista[1]] if self.df.loc[(self.df["School"] == lista[1])]["POSTSEASON"].values[0] == '2ND' else [lista[1], lista[0]]

            else:
                round_dict = {}
                for region in regions:
                    lista = generated[rounds[j-1]][region]
                    temp = []
                    for i in range(0, len(lista), 2):
                        temp.append([lista[i][0], lista[i+1][0]] if self.df.loc[(self.df["School"] == lista[i+1][0])]["POSTSEASON"].values[0] == round else [lista[i+1][0], lista[i][0]])
                    round_dict[region] = temp
                generated[round] = round_dict
                        
        return generated

    def predict_bracket(self):
        for round in self.bracket.keys():
            if round != 'Champions':
                for region in self.bracket[round]:   
                        if self.bracket[round][region] == []:
                            continue
                        print(round, region)
                        if round == 'F4':
                            print(self.bracket[round][region])
                            print("WINNER: ", self.bracket[round][region][0])
                        else:
                            for matchup in self.bracket[round][region]:
                                print(matchup)
                                print("WINNER: ", matchup[0])
            else:
                print("FINAL ",self.bracket[round])
                print("WINNER: ", self.bracket[round][0])


    def predict_games(self):
        pass