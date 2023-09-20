from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

website = "https://finance.yahoo.com/"

#response = requests.get(website)
#content = response.text

#soup = BeautifulSoup(content, 'lxml')

#crypto_link = soup.find('a',class_=re.compile('applet'),title ='Crypto',href=True)
#response = requests.get(f"{website}/{crypto_link['href']}")
#content = response.text

#soup = BeautifulSoup(content, 'lxml')

# Pagination
n = 0
last_page = 10

symbols = []
names = []
prices = []
changes = []
changes_per = []
market_caps = []
total_volumes = []
circulating_supplies = []


for x in range(last_page):
    response = requests.get(f"{website}/crypto/?count=25&offset={n}")
    content = response.text
    soup = BeautifulSoup(content,'lxml')
    box = soup.find('tbody').find_all('tr')
    
    # Get tabular data

    for element in box:
        data = element.find_all('td')
        symbols.append(data[0].find('a',class_='Fw(600) C($linkColor)',href=True).get_text())
        names.append(data[1].get_text())
        prices.append(data[2].find('fin-streamer').get_text())
        changes.append(data[3].find('fin-streamer').get_text())
        changes_per.append(data[4].find('fin-streamer').get_text())
        market_caps.append(data[5].find('fin-streamer').get_text())
        total_volumes.append(data[7].get_text())
        circulating_supplies.append(data[8].get_text())
    
    n = n + 25
    
# Create Dataframe

df = pd.DataFrame({"Symbol":symbols,
                   "Name":names,
                   "Price":prices,
                   "Change":changes,
                   "% Change":changes_per,
                   "Market Cap":market_caps,
                   "Total Volume":total_volumes,
                   "Circulating Supply":circulating_supplies})

print(df.head())
df.to_csv("./Projects/BeautifulSoup/crypto.csv")


