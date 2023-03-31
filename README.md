# bot-hzakharenko

### March 31 update
This week, I finished setting up the web scraping portion of the bot. I was able to use Selenium to load the webpage and push the "More Results" button so that I can scrape the date_updated for the 40 most recently updated datasets every day.

The next thing I did was set up my code to load in the original csv file (from the initial run of the RSS feed) and only add to it when there are new things. Since I need to scrape the RSS feed to get information about datasets when they are published, I saved an initial file, and then I will scrape the RSS feed every day and append rows where the published date is later than the latest date in the saved csv file, effectively only saving new items when they are added.

I also set it up so that my smaller dataframe with 40 titles and date_updated columns dates joins with the rss_feed so that I can slowly build a csv that includes both date published and the date updated.

Up next, I need to set up a Slack bot to send me a message if there is a date_updated in this dataframe that is equal to today's date. I want this message to deliver to me the number of datasets updated, and then a bulleted list with all of the information from that row in the dataframe (link, title, description, published data, and date updated).

Once I have my Slack bot set up, the last step is to set up a yaml file in Github to run the file every day, so that my Slack bot can update me daily if there are new datasets updated.

I think that I am on track to complete my bot by the end of next week. I want to keep the Slack bot message simple right now, but over time, I can consider adding more details or tailoring what I scrape to something specific if I find the results I am getting not useful.