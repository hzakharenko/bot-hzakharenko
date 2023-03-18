from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#followed these steps to get google chrome driver to work in codespaces: https://www.keeganleary.com/setting-up-chrome-and-selenium-with-python-on-a-virtual-private-server-digital-ocean/

options = Options()
options.headless = True
driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
driver.get("https://opendata.dc.gov/search?sort=-modified")
time.sleep(15)
#button = driver.find_elements(By.CLASS_NAME, "btn more-results link-color-primary")
#button = driver.find_elements("xpath", '//*[@id="ember120"]/button[1]')
#button.click()

plain_text = driver.page_source
soup = BeautifulSoup(plain_text, 'lxml')

#To get this line, I asked ChatGPT: "how do i capture data-test="metadata-col-1-item-1" with beautiful soup in python"
items = soup.find_all(attrs={"data-test": "metadata-col-1-item-1"})

for item in items:
    print(item.text.strip())

driver.quit()

"""This gets me all the information I need! Need to get selenium to push the 
button for me to get more results though, as there appear to be more than 20
datasets updated per day. Right now, I can't get it to find the button."""