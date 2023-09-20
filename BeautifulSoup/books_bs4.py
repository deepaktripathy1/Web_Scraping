from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from word2number import w2n

website = "http://books.toscrape.com/"

response = requests.get(website)
content = response.text

soup = BeautifulSoup(content, "lxml")
# print(soup.prettify())

box = soup.find_all('h3')
links = []
for element in box:
    link = element.find('a')
    links.append(link['href']) # get the links
    
titles = []
prices = []
availability = []
rating = []
descriptions = []
for link in links:
    webpage = f"{website}/{link}"
    response = requests.get(webpage)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article',class_='product_page')
    try:
        title = box.find('h1').get_text() # get title
        titles.append(title)
        price = box.find('p',class_='price_color').get_text() # get price
        prices.append(price)
        # get availability
        available = box.find('p',class_='instock availability').get_text()
        availability.append(' '.join(available.split()).lstrip('\n').rstrip('\n'))
        star_rating = box.find('p',class_=re.compile('star-rating'))['class'][1] # get rating
        rating.append(w2n.word_to_num(star_rating)) # convert word to integer using word2num
        description = box.find('p',class_=False).get_text() # get product description
        descriptions.append(description)
    except:
        pass
    
# Create dataframe

df = pd.DataFrame({"title":titles,
                   "link":links,
                   "price":prices,
                   "rating":rating,
                   "availability":availability,
                   "description":descriptions})

print(df.head())

# Save to csv file

df.to_csv("./Projects/books_sample.csv")

print("Process completed")



    
