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

titles = []
categories = []
prices = []
ratings = []
availability = []
descriptions = []
links = []


for x in range(5): # for 5 pages only
    if x == 0:
        main_url = website
        driver.get(main_url)
        
    matches = driver.find_elements(By.XPATH, value='//h3')
    book_links = []
    for match in matches:
        product_links = match.find_element(By.TAG_NAME, value= 'a').get_attribute('href')
        book_links.append(product_links)
        links.append(product_links)
    for link in book_links:
        driver.get(link)
        try:
            titles.append(driver.find_element(By.XPATH, value='//h1').text)
            categories.append(driver.find_elements(By.XPATH, value='//ul[@class="breadcrumb"]//a[contains(@href,"books")]')[1].text)
            prices.append(driver.find_element(By.XPATH, value='//p[@class="price_color"]').text)
            ratings.append(driver.find_element(By.XPATH, value='//p[contains(@class,"star-rating")]').get_attribute('class'))
            available = driver.find_element(By.XPATH, value='//p[@class="instock availability"]').text
            availability.append(' '.join(available.split()).lstrip('\n').rstrip('\n'))
            descriptions.append(driver.find_element(By.XPATH, value='//p[not(@class)]').text)
        except:
            pass
        
    driver.get(main_url)
    time.sleep(2)
    next_page = driver.find_element(By.XPATH, value='//li[@class="next"]//a[@href]')
    if next_page:
        next_url = next_page.get_attribute('href')
        main_url = next_url
        driver.get(next_url)
    else:
        break

df = pd.DataFrame({"title": titles,
                   "category":categories,
                   "price": prices, 
                   "rating": ratings, 
                   "availability": availability,
                   "description":descriptions,
                   "links":links})

print(df.head())

df.to_csv("./Projects/Selenium/all_books_sel_pagination.csv")