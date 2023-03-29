import pandas as pd
import os

map = {'Alabama St.':'Alabama State','Albany':'Albany (NY)','Alcorn St.':'Alcorn State','Appalachian St.':'Appalachian State',
'Arizona St.':'Arizona State','Arkansas St.':'Arkansas State','Arkansas Pine Bluff':'Arkansas-Pine Bluff','Ball St.':'Ball State',
'Boise St.':'Boise State','Bowling Green':'Bowling Green State','BYU':'Brigham Young','Cal St. Bakersfield':'Cal State Bakersfield',
'Cal St. Fullerton':'Cal State Fullerton','Cal St. Northridge':'Cal State Northridge','Chicago St.':'Chicago State',
'Cleveland St.':'Cleveland State','Colorado St.':'Colorado State','Coppin St.':'Coppin State','Delaware St.':'Delaware State',
'Detroit':'Detroit Mercy','East Tennessee St.':'East Tennessee State','FIU':'Florida International','Florida St.':'Florida State',
'Fresno St.':'Fresno State','Georgia St.':'Georgia State','Grambling St.':'Grambling','Houston Baptist':'Houston Christian',
'Idaho St.':'Idaho State','Illinois Chicago':'Illinois-Chicago','Illinois St.':'Illinois State','Iowa St.':'Iowa State',
'IPFW':'Purdue-Fort Wayne','Jackson St.':'Jackson State','Jacksonville St.':'Jacksonville State','Kansas St.':'Kansas State',
'Kennesaw St.':'Kennesaw State','Kent St.':'Kent State','Arkansas Little Rock':'Little Rock','LIU Brooklyn':'Long Island University',
'Long Beach St.':'Long Beach State','Louisiana Lafayette':'Louisiana','Louisiana Monroe':'Louisiana-Monroe','Loyola Chicago':'Loyola (IL)',
'Loyola MD':'Loyola (MD)','LSU':'Louisiana State','McNeese St.':'McNeese State','Miami FL':'Miami (FL)','Miami OH':'Miami (OH)',
'Michigan St.':'Michigan State','Mississippi St.':'Mississippi State','Mississippi Valley St.':'Mississippi Valley State',
'Missouri St.':'Missouri State','Montana St.':'Montana State','Morehead St.':'Morehead State','Morgan St.':'Morgan State',
'Murray St.':'Murray State','North Carolina St.':'NC State','Nebraska Omaha':'Omaha','New Mexico St.':'New Mexico State',
'Nicholls St.':'Nicholls State','Norfolk St.':'Norfolk State','North Dakota St.':'North Dakota State',
'Northwestern St.':'Northwestern State','Ohio St.':'Ohio State','Oklahoma St.':'Oklahoma State','Oregon St.':'Oregon State',
'Penn St.':'Penn State','Portland St.':'Portland State','Prairie View A&M':'Prairie View','Sacramento St.':'Sacramento State',
'Saint Mary\'s':'Saint Mary\'s (CA)','Sam Houston St.':'Sam Houston State','San Diego St.':'San Diego State',
'San Jose St.':'San Jose State','SMU':'Southern Methodist','South Carolina St.':'South Carolina State',
'South Dakota St.':'South Dakota State','Southeast Missouri St.':'Southeast Missouri State','Southern Miss':'Southern Mississippi',
'St. Francis NY':'St. Francis (NY)','St. John\'s':'St. John\'s (NY)','Tennessee Martin':'Tennessee-Martin',
'Tennessee St.':'Tennessee State','Texas A&M Corpus Chris':'Texas A&M-Corpus Christi','Texas St.':'Texas State',
'UCF':'Central Florida','UMBC':'Maryland-Baltimore County','UMKC':'Kansas City','UNLV':'Nevada-Las Vegas',
'USC':'Southern California','USC Upstate':'South Carolina Upstate','Utah St.':'Utah State','VCU':'Virginia Commonwealth',
'Washington St.':'Washington State','Weber St.':'Weber State','Wichita St.':'Wichita State','Wright St.':'Wright State',
'Youngstown St.':'Youngstown State','Gardner Webb':'Gardner-Webb','Penn':'Pennsylvania'}

def remove_schools(data, intersect):
    global map
    index = data[~data['TEAM'].isin(intersect)].index
    data.drop(index, inplace=True)

    data.replace(map, inplace=True)

    return data

def find_intersect(df_list):
    intersect = set(df_list[0].TEAM)
    for i in range(1,len(df_list)):
        intersect = intersect & set(df_list[i].TEAM)
    
    for i in range(0,len(df_list)):
        if i != 7:
            playoff = set(df_list[i].loc[df_list[i].SEED != 'NA', 'TEAM'])
            intersect.update(playoff)
    
    return intersect


path = './data/teamSeeds/'
new_path = './data/teamSeedsProc/'
dir_list = os.listdir(path)
df_list = []

for csv in dir_list:
    df_list.append(pd.read_csv(path + csv))

intersect = find_intersect(df_list)

for i,csv in enumerate(dir_list):
    df_list[i] = remove_schools(df_list[i], intersect)
    print(len(df_list[i]))
    df_list[i].to_csv(new_path + csv, index=False)
