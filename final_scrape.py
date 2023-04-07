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
import datetime
import os
from slack import WebClient
from slack.errors import SlackApiError

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

#sort by date of published so that most recent date is last
rss_df['published'] = pd.to_datetime(rss_df['published'])
rss_df = rss_df.sort_values(by='published', ascending=True)
print(len(rss_df))

original_rss = pd.read_csv('final_df.csv')
#if the length of the rss_df is longer than length of rss_df.csv: to get this, I used some lines from the question I asked chatGPT: scrape and create dataframe every day using beautiful soup, but retain whats already there and only include new rows
if len(rss_df) > len(original_rss):
    #calculate how many new entries were added and print note
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

#create a dataframe with the values scraped: to get this I asked chatGPT: Scrape all titles and dates in a html page using beautiful soup and turn that into a dataframe
data = []
for title, date_updated in zip(titles, pg_date_updated):
    data.append({'title': title.text.strip(), 'date_updated': date_updated.text.strip()})
daily_updates_df = pd.DataFrame(data)
print(daily_updates_df)

#join this to the RSS dataframe by title
#final_df = original_rss.merge(daily_updates_df, on='title', how='left')
#final_df = pd.merge(original_rss, daily_updates_df, on='title', how='left')
original_rss.update(daily_updates_df)
print(original_rss)

# Save the final DataFrame to a CSV file
original_rss.to_csv('final_df.csv', index=False)

###
# Report new updates to datasets using Slack bot
###
#Set latest date -- filter for it in dataframe -- if length > 0, send message
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
print(current_date)

#create a date column from final df with just date updated
original_rss['date'] = pd.to_datetime(original_rss['date_updated'], format='%B %d, %Y')

original_rss['date'] = original_rss['date'].dt.date.astype(str)

df_filtered = original_rss.dropna(subset=['date'], how='any')
print(df_filtered)

new_rows = original_rss[original_rss['date'] == current_date]
print(new_rows)
url = "https://github.com/NewsAppsUMD/bot-hzakharenko/blob/main/new_rows.csv"

if len(new_rows) > 0:
    #bullet_list = "- title: " + new_rows["title"]+"\n"
    #bullet_list = bullet_list.to_list()
   # bullet_list = "".join(bullet_list)
   new_rows.to_csv('new_rows.csv', index=False)
   msg = f"There have been {len(new_rows)} new rows datasets updated today! See more: {url}"

#set up Slack token stuff
slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)


if len(new_rows) > 0:
    try:
        response = client.chat_postMessage(
            channel="slack-bots",
            text=msg,
            unfurl_links=True, 
            unfurl_media=True
        )
        print("success!")
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
else:
        try:
            response = client.chat_postMessage(
            channel="slack-bots",
            text="no new updates today!",
            unfurl_links=True, 
            unfurl_media=True
        )
            print("success!")
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
