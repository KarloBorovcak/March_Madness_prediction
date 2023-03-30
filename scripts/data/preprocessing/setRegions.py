import pandas as pd

years = {2022: {'east': {'Indiana', 'Baylor', 'Virginia Tech', 'Akron', "St. Peter's", 'Norfolk State', 'Yale', 'Texas', 'UNC', 'Murray State', 'Kentucky', 'UCLA', 'Purdue', 'San Francisco', 'Marquette', "Saint Mary's"}, 'midwest': {'Texas Southern', 'Creighton', 'Kansas', 'USC', 'LSU', 'Miami (FL)', 'Iowa State', 'Colgate', 'South Dakota State', 'Wisconsin', 'Providence', 'San Diego State', 'Jacksonville State', 'Richmond', 'Iowa', 'Auburn'}, 'south': {'UAB', 'Loyola (IL)', 'Seton Hall', 'Michigan', 'Tennessee', 'Villanova', 'Wright State', 'Colorado State', 'Houston', 'Chattanooga', 'Ohio State', 'Arizona', 'Delaware', 'Illinois', 'Longwood', 'TCU'}, 'west': {'Gonzaga', 'UConn', 'Arkansas', 'Vermont', 'Montana State', 'Georgia State', 'Duke', 'Cal State Fullerton', 'New Mexico State', 'Boise State', 'Michigan State', 'Davidson', 'Notre Dame', 'Memphis', 'Alabama', 'Texas Tech'}}}
rename = {'UC-Davis':'UC Davis','UCF':'Central Florida', 'UCSB':'UC Santa Barbara','USC':'Southern California',
'UC-Irvine':'UC Irvine','UMBC':'Maryland-Baltimore County','UNC':'North Carolina','St. Joseph\'s':'Saint Joseph\'s',
'LSU':'Louisiana State','BYU':'Brigham Young','Pitt':'Pittsburgh','VCU':'Virginia Commonwealth',
'ETSU':'East Tennessee State','Ole Miss':'Mississippi','LIU':'Long Island University',
'SMU':'Southern Methodist','UConn':'Connecticut','Saint Mary\'s':'Saint Mary\'s (CA)',
'Penn':'Pennsylvania','UMass':'Massachusetts'}



df = pd.read_csv('./data/clean/2022-school-stats.csv')

# years_set = set()
# for year in years:
#     for region in years[year]:
#         years_set = years_set | years[year][region]

# schools = set(df['School'].tolist())
# final = schools ^ years_set

df2 = pd.DataFrame(columns=['School', 'Year', 'REGION'])

for year in years:
    for region in years[year]:
        for team in years[year][region]:
            if team in rename.keys():
                df2.loc[len(df2.index)] = [rename[team], year, region] 
            else:
                df2.loc[len(df2.index)] = [team, year, region]

for i in range(2022, 2023):
    if i != 2020:
        df = pd.read_csv('./data/clean/' + str(i) + '-school-stats.csv')

        df3 = pd.merge(df, df2.loc[df2['Year'] == i], how='outer', on='School').drop('Year', axis=1)
        print(df3.columns)
        df3['REGION'] = df3['REGION'].str.upper()

        df3.to_csv('./data/clean/' + str(i) + '-school-stats.csv', index=False)
        
