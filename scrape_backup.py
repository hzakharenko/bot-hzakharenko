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
rss_df = pd.DataFrame(articles)

# print the dataframe
#print(rss_df.head())
#print(len(rss_df))
#rss_df.to_csv('final_df.csv', index=False)

#read in original rss_df
original_rss = pd.read_csv('final_df.csv')

#if the length of the rss_df is longer than length of rss_df.csv: to get this, I used some lines from the question I asked chatGPT: scrape and create dataframe every day using beautiful soup, but retain whats already there and only include new rows
if len(rss_df) > len(original_rss):
    new_datasets = len(rss_df) - len(original_rss)
    print(f"There has been an update to the RSS feed! There were {new_datasets} new datasets published.")

    # Get the latest date in the existing DataFrame
    latest_date = pd.to_datetime(original_rss['published'].iloc[-1])

    # Filter the new DataFrame to keep only rows with a date greater than the latest date in the existing DataFrame
    rss_df = rss_df[pd.to_datetime(rss_df['published']) > latest_date]

    # Append the new DataFrame to the existing DataFrame
    original_rss = original_rss.append(rss_df, ignore_index=True)


###
#Pull new documents by grabbing Date_updated to add to dataframe with BeautifulSoup
###

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

# #print all the titles of the datasets on a page
# for title in titles:
#     print(title.text.strip())

# #print all the date updates on a page
# for date_updated in pg_date_updated:
#     print(date_updated.text.strip())

#create a dataframe with the values scraped: to get this I asked chatGPT: Scrape all titles and dates in a html page using beautiful soup and turn that into a dataframe
data = []
for title, date_updated in zip(titles, pg_date_updated):
    data.append({'title': title.text.strip(), 'date_updated': date_updated.text.strip()})
daily_updates_df = pd.DataFrame(data)
print(daily_updates_df)

#join this to the RSS dataframe by title
final_df = original_rss.merge(daily_updates_df, on='title', how='left')
print(final_df)


# Save the final DataFrame to a CSV file
final_df.to_csv('final_df.csv', index=False)

#TO DO
    #update code so it only adds new records, not overwriting it
    #set Slack bot to report any new rows (where date_updated = today)
    #yaml file to run every day


driver.quit()

"""Wed 3-29 update: Worked to get dataframess to update only when there is
new information to the saved csv. Next steps: Confirm this is working properly, 
then set up Slack bot to send a message if there are new updates.Then, set up
yaml code to run this file every day"""
