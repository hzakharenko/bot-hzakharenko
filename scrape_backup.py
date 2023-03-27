#apt-get update
#apt install chromium-chromedriver
import csv
import requests
import json
from bs4 import BeautifulSoup
import feedparser
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


#Create a daataframe of all documents in Open_Data_DC

# define RSS feed URL
rss_url = 'https://datahub-dc-dcgis.hub.arcgis.com/api/feed/rss/2.0'

# parse the RSS feed
feed = feedparser.parse(rss_url)

# create a list of dictionaries containing the article information
articles = []
for entry in feed.entries:
    articles.append({
        'link': entry.link,
        'title': entry.title,
        'description': entry.description,
        'published': entry.published
    })

# create a dataframe from the list of dictionaries
df = pd.DataFrame(articles)

# print the dataframe
print(df.head())
print(len(df))

#Pull new documents by grabbing Date_updated to add to dataframe with BeautifulSoup

#followed these steps to get google chrome driver to work in codespaces: https://www.keeganleary.com/setting-up-chrome-and-selenium-with-python-on-a-virtual-private-server-digital-ocean/

options = Options()
options.headless = True
driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
driver.get("https://opendata.dc.gov/search?collection=Dataset&sort=-modified")
time.sleep(15)
#button = driver.find_elements(By.CLASS_NAME, "btn more-results link-color-primary")
#button = driver.find_elements("xpath", '//*[@id="ember120"]/button[1]')
#button.click()

plain_text = driver.page_source
soup = BeautifulSoup(plain_text, 'lxml')

#To get this line, I asked ChatGPT: "how do i capture data-test="metadata-col-1-item-1" with beautiful soup in python"
titles = soup.find_all(attrs={"data-test": "list-card-title"})
pg_date_updated = soup.find_all(attrs={"data-test": "metadata-col-1-item-1"})

#print all the titles of the datasets on a page
for title in titles:
    print(title.text.strip())

#print all the date updates on a page
for date_updated in pg_date_updated:
    print(date_updated.text.strip())

driver.quit()

"""This gets me all the information I need! Need to get selenium to push the 
button for me to get more results though, as there appear to be more than 20
datasets updated per day. Right now, I can't get it to find the button."""
