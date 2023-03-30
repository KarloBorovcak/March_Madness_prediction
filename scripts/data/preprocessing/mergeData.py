import pandas as pd
import os

path = './data/teamSeedsProc/'
dir_list = os.listdir(path)
df_list = []

for i,csv in enumerate(dir_list):
    df_list.append(pd.read_csv(path + csv))
    df_list[i].fillna('NA', inplace=True)


playoff = set(df_list[0].loc[df_list[0].SEED != 'NA', 'TEAM'])

for i in range(1,len(dir_list)):
    if i != 6:
        playoff.update(set(df_list[i].loc[df_list[i].SEED != 'NA', 'TEAM']))


path2 = './data/cleanTeamStats/'
dir_list2 = os.listdir(path2)
df_list2 = []

for i,csv in enumerate(dir_list2):
    df_list2.append(pd.read_csv(path2 + csv))
    df_list2[i].fillna('NA', inplace=True)

new_df_list = []

for i in range(len(dir_list)):
    df_list[i] = df_list[i].loc[df_list[i].TEAM.isin(playoff)]
    df_list2[i] = df_list2[i].loc[df_list2[i].School.isin(playoff)] 
    df_list[i].rename(columns = {'TEAM':'School'}, inplace = True)

df_list[-1]["POSTSEASON"] = ""
new_path = './data/statsAndSeeds/'


for i in range(len(df_list)):
    temp1 = df_list2[i]
    temp2 = df_list[i].filter(["School","SEED","POSTSEASON"], axis=1)
    temp = pd.merge(temp1, temp2, how='outer', on='School')
    new_df_list.append(temp)

for i,csv in enumerate(dir_list2):
    print(len(new_df_list[i]))
    new_df_list[i].to_csv(new_path + csv, index=False)
