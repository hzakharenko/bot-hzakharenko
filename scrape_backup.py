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
time.sleep(2)
button = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/button[1]').click()
time.sleep(2)

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

"""Mon 3-27 update: got button clicked and I am now collecting title and date
updated for the first 40 items on the page, enough to cover daily updates. Next 
steps: figure out how to attach this to the RSS Feed dataframe (joining on 
dataset title) and then spit that csv out to Github. Set a time parameter for 
if the date == today --> Slack Bot does something. Then, set up yaml code to run
this file every day"""
