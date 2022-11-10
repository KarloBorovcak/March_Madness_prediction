from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd


source = requests.get("https://www.sports-reference.com/cbb/seasons/2022-opponent-stats.html")

soup = BeautifulSoup(source.text, 'html.parser')

stats = soup.find('pre' ,id='csv_basic_opp_stats')

print(stats)