from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time

website = "https://finance.yahoo.com/crypto/"
path = "C:/Users/deepa/Documents/AI-ML/WebScraping/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.get(website)

# Pagination
n = 0

symbols = []
names = []
prices = []
changes = []
changes_per = []
market_caps = []
total_volumes = []
circulating_supplies = []

for x in range(10):
    if x > 0:
        driver.get(f"{website}?count=25&offset={n}")
    
    table = driver.find_elements(By.XPATH, value='//tbody/tr')
    for row in table:
        data = row.find_elements(By.XPATH, value= './td')
        symbols.append(data[0].find_element(By.XPATH, value= './a').text)
        names.append(data[1].text)
        prices.append(data[2].find_element(By.XPATH, value='./fin-streamer').text)
        changes.append(data[3].find_element(By.XPATH, value='./fin-streamer').text)
        changes_per.append(data[4].find_element(By.XPATH, value='./fin-streamer').text)
        market_caps.append(data[5].find_element(By.XPATH, value='./fin-streamer').text)
        total_volumes.append(data[7].text)
        circulating_supplies.append(data[8].text)
        
    n += 25
    
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
df.to_csv("./Projects/Selenium/crypto_sel.csv")
    