from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from word2number import w2n

website = "http://books.toscrape.com/"
link_url = "http://books.toscrape.com/catalogue/"

links = []
titles = []
prices = []
availability = []
rating = []
descriptions = []


for x in range(10): # get data for first 10 pages only
    if x == 0:
        main_url = website
    elif x == 1:
        main_url = website + url
    else:
        main_url = link_url + url
    
    response = requests.get(main_url)
    content = response.text

    soup = BeautifulSoup(content, "lxml")
    # print(soup.prettify())
    
    all_links_element_a = soup.find_all('a',href=True)
    
    box = soup.find_all('h3')
    weblinks = []
    for element in box:
        link = element.find('a')
        weblinks.append(link['href'])
        links.append(link['href']) # get the links
            
    for link in weblinks:
        if x == 0:
            webpage = f"{website}/{link}"
        else:
            webpage = f"{link_url}/{link}"

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

    for a in all_links_element_a:
        if a.get_text() == 'next':
            url = a.get('href')
    
# Create dataframe

d = {"title":titles,
    "link":links,
    "price":prices,
    "rating":rating,
    "availability":availability,
    "description":descriptions}

df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in d.items()]))

print(df.head())

# Save to csv file

df.to_csv("./Projects/all_books_pagination.csv")

print("Process completed")