import csv
import requests
import json
from bs4 import BeautifulSoup
import feedparser
import pandas as pd

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
