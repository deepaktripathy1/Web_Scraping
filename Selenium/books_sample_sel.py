from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from word2number import w2n
import pandas as pd
import string
import re
import time

website = "http://books.toscrape.com/"
path = "C:/Users/deepa/Documents/AI-ML/WebScraping/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)

matches = driver.find_elements(By.XPATH, value='//h3') # get product links

links = []
titles = []
categories = []
prices = []
ratings = []
availability = []
descriptions = []

for match in matches:
    product_links = match.find_element(By.TAG_NAME, value= 'a').get_attribute('href')
    links.append(product_links)

for link in links:
    driver.get(link)
    titles.append(driver.find_element(By.XPATH, value='//h1').text)
    categories.append(driver.find_element(By.XPATH, value='//ul[@class="breadcrumb"]//a[contains(@href,"books")]').text)
    prices.append(driver.find_element(By.XPATH, value='//p[@class="price_color"]').text)
    ratings.append(driver.find_element(By.XPATH, value='//p[contains(@class,"star-rating")]').get_attribute('class'))
    available = driver.find_element(By.XPATH, value='//p[@class="instock availability"]').text
    availability.append(' '.join(available.split()).lstrip('\n').rstrip('\n'))
    descriptions.append(driver.find_element(By.XPATH, value='//p[not(@class)]').text)
    

df = pd.DataFrame({"title": titles, 
                   "price": prices, 
                   "rating": ratings, 
                   "availability": availability,
                   "description":descriptions,
                   "links":links})

df.to_csv("./Projects/Selenium/books_sample_selenium.csv")
print(df)
    