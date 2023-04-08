# bot-hzakharenko

### Final bot submission update (4/8/23)
This week, I worked towards the final steps of my bot. Since I had spent the last week finalizing how I was scraping the information, this week I focused on making sure my code could run and update every day, setting up a Slack message to best communicate this information, and setting up a YAML file to run this code through Github actions once a day.

Through this process, I learned that the initial format I had set up for my message (reporting each new row's information-- including date published, title, link, and description) was too much because sometimes I could be reporting 40 new rows of information. I also noticed that even just putting the titles made the message look too long. So, I decided I would just report the number of new updates in the Slack message and link to a dataframe showing the new rows. Ideally, I would want this to be a datasette, but I didn't have the time to set that up and figure out how to get a link to share, so for now, I linked it to a searchable dataframe in Github. Another issue I found was that one day, I noticed that there were 60+ new datasets updated, and the max I am scraping right now is 40. 

Looking foward, if this bot were able to take input from users, I would want users to be able to query the bot on the types of datasets that had been updated. I know that these datasets are categorized on the website, and if I can obtain the metadata for this to add to what I already have, it would be very helpful for users to be able to ask questions like "Was there anything updated on transportation?" and for the bot to spit out the titles of any new datasets that were put in this category.

I also had issues figuring out how to best update my data. I ran into some confusing errors that were making new date_updated columns instead of overriding the information I had in the column already, so I moved to use .update() instead of a join. However, this method might introduce different errors.

Lastly, I worked on adding a YAML file to my GitHub and getting it to run. While the YAML file successfully runs on schedule, it gets a "not_authed" error for Slack, even though I put my auth code in the actions repo environment. 

Overall, I spent this week thinking I was adding finishing touches and running into many more problems than I had in weeks past. However, it was fun to create workarounds for things that I thought were going to work up until the last minute, and I plan to continue working on this until my bot runs successfully, because I think the information it provides is very helpful to me and others.

I think that in the next week, I should be able to clean my code and fix up my YAML file issues (if possible) to get my code to run daily. I plan to move on to a different task for the final project instead of continuing to improve upon my bot.