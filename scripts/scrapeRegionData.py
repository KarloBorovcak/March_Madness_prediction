from bs4 import BeautifulSoup
import requests

years = {}
teams = {"east": set(), "midwest": set(), "south": set(), "west": set()}
regions = ["east", "midwest", "south", "west"]


for i in range(2014, 2022):
    if i != 2020:
        teams = {"east": set(), "midwest": set(), "south": set(), "west": set()}
        
        URL = "https://www.sports-reference.com/cbb/postseason/" + str(i) + "-ncaa.html"

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")   

        for region in regions:
            results = soup.find(id=region)

            f4 = results.find("p")
            if f4 != None:
                f4 = f4.find_all("a")
                for team in f4:
                    if not team.text.isnumeric() and not team.text[0:2] == 'at':
                        teams[region] = teams[region] | set([team.text])

            results = results.find(class_="round")
            results = results.find_all("a")

            for result in results:
                if not result.text.isnumeric() and not result.text[0:2] == 'at':
                    teams[region] = teams[region] | set([result.text])
        
        years[i] = teams




# for year in years:
#     suma = 0
#     for region in years[year]:
#         suma += len(years[year][region])
#     print(suma)
print(years)
