import csv
import requests
import json
from bs4 import BeautifulSoup

url = 'https://opendata.arcgis.com/api/v3/search'
payload = {"agg":{"fields":"type,access,source,categories,license,tags,region,sector","size":"100"},"filter":{"collection":"any(Dataset)"},"catalog":{"groupIds":"any(6dc06587ef9a4569b2574e92665e515d,489e982ea160416bb62a8247175ad9c0,d3ad991e7c9447bf81c3ef4fac5f6696,6eba62e38f094906974b0b87956b7a31,ee2a1b12c6b24c2ea0f39ec5023508ba,95c59d84749742b7ad1e135c6e685009,ec224dd0c2294755a0e232d784eb1172,72c19e0ed89641ac83045a4597a6c9dc,4c106214b9ba46aeb028a16134fa71cc,e24f6a47d94c493d99d6d99a8d77b3db,e6c5e47b278342b9baf21632ea2f3b34,0204ece8c0344982a8923e43e93bbd13,a7749d01300f4f87a8769d26a5df2181,6f754c5a004542bb9f1f8830258aa794,586b466e82834506b1754a3b94bc5d3a,685c2780f30644e3992194a454c2db50,42f1e95acd8845da8c7426a414aefb33,95b53f8cb48c418d8e8a2f5827c5944b,7e97b9f459934994a37300b2be196ba2,6664e0b92948483ab633b3080d466122,0fd6c262970c4442a66e57e3deb270d2,d03638459011457f9a7152011ad0ff82,3f8def9a54d948d4bee9a72c62a14d42,f5eb4bac6ed544d5be1dd7e5e69652d1,38f272d281d348ddad8dbbcfed515e05,3cfdba546f1e40b0b430127c7cefd384,9f22ca286c814193bc0f87106df548fb,5ff18aacf97f4008a277fa6c81cdb5df,0ef7f4b207e245b28b235a896be1c0f3,62be2f179f674941b393f1c9bc8ca73e,821474b35eb74c1b899f3b0f75e42ab8,35d3981a82874e01b1c1df0aef7227c8,3d738aca3d274f6c8748256738e83f14,73fa9cc1ce8e488b8c822c1c017887d6,b7d32c689e044f0997a1fbd5c9462249,696e1f4cb4f4464fa3ae72370f1d1eeb,f397df808a7d48b59c7417f370413e6b,d37febcec5094c719eb244d59d3ae08d,08cada661e7c41748df5a7042d3375d7,e4ea8f08ec834a53bd067676fc09274a,f3de8399eb0f493b84c8bbe076079ead,e60a958b3e8340b7ac3549ced5ec5157,e5eae38d52fa46248918d57a91b511a0,1886eed80b81426bb87336170ebfa2b1,df93506fd2b2441e8773845f213d4086,d89dd1d76bc647089128129b2507b734,7d187f81f7594617b8d496aefedc0478,7d332794e2e54004995c5c50aaad6059,499467eb06a546968283905708e7c05e,d9592387328c447c89fa07e8f4d5f2ff,9f70eb9a4f2048b3920a476427467eea,1202470439f14a199d8029a92fdb5dad,fd8b3227eee74d509d93fa127b255fac,49b26f3e86e74654a632be7adf9eca3d)","initiativeId":"any(962a8b7095c743e3b521ed2765ce7930)"}}
response = requests.post(url, json=payload)

url = 'https://opendata.arcgis.com/api/v3/search?agg%5Bfields%5D=type%2Caccess%2Csource%2Ccategories%2Clicense%2Ctags%2Cregion%2Csector&agg%5Bsize%5D=100&filter%5Bcollection%5D=any%28Dataset%29&catalog%5BgroupIds%5D=any%286dc06587ef9a4569b2574e92665e515d%2C489e982ea160416bb62a8247175ad9c0%2Cd3ad991e7c9447bf81c3ef4fac5f6696%2C6eba62e38f094906974b0b87956b7a31%2Cee2a1b12c6b24c2ea0f39ec5023508ba%2C95c59d84749742b7ad1e135c6e685009%2Cec224dd0c2294755a0e232d784eb1172%2C72c19e0ed89641ac83045a4597a6c9dc%2C4c106214b9ba46aeb028a16134fa71cc%2Ce24f6a47d94c493d99d6d99a8d77b3db%2Ce6c5e47b278342b9baf21632ea2f3b34%2C0204ece8c0344982a8923e43e93bbd13%2Ca7749d01300f4f87a8769d26a5df2181%2C6f754c5a004542bb9f1f8830258aa794%2C586b466e82834506b1754a3b94bc5d3a%2C685c2780f30644e3992194a454c2db50%2C42f1e95acd8845da8c7426a414aefb33%2C95b53f8cb48c418d8e8a2f5827c5944b%2C7e97b9f459934994a37300b2be196ba2%2C6664e0b92948483ab633b3080d466122%2C0fd6c262970c4442a66e57e3deb270d2%2Cd03638459011457f9a7152011ad0ff82%2C3f8def9a54d948d4bee9a72c62a14d42%2Cf5eb4bac6ed544d5be1dd7e5e69652d1%2C38f272d281d348ddad8dbbcfed515e05%2C3cfdba546f1e40b0b430127c7cefd384%2C9f22ca286c814193bc0f87106df548fb%2C5ff18aacf97f4008a277fa6c81cdb5df%2C0ef7f4b207e245b28b235a896be1c0f3%2C62be2f179f674941b393f1c9bc8ca73e%2C821474b35eb74c1b899f3b0f75e42ab8%2C35d3981a82874e01b1c1df0aef7227c8%2C3d738aca3d274f6c8748256738e83f14%2C73fa9cc1ce8e488b8c822c1c017887d6%2Cb7d32c689e044f0997a1fbd5c9462249%2C696e1f4cb4f4464fa3ae72370f1d1eeb%2Cf397df808a7d48b59c7417f370413e6b%2Cd37febcec5094c719eb244d59d3ae08d%2C08cada661e7c41748df5a7042d3375d7%2Ce4ea8f08ec834a53bd067676fc09274a%2Cf3de8399eb0f493b84c8bbe076079ead%2Ce60a958b3e8340b7ac3549ced5ec5157%2Ce5eae38d52fa46248918d57a91b511a0%2C1886eed80b81426bb87336170ebfa2b1%2Cdf93506fd2b2441e8773845f213d4086%2Cd89dd1d76bc647089128129b2507b734%2C7d187f81f7594617b8d496aefedc0478%2C7d332794e2e54004995c5c50aaad6059%2C499467eb06a546968283905708e7c05e%2Cd9592387328c447c89fa07e8f4d5f2ff%2C9f70eb9a4f2048b3920a476427467eea%2C1202470439f14a199d8029a92fdb5dad%2Cfd8b3227eee74d509d93fa127b255fac%2C49b26f3e86e74654a632be7adf9eca3d%29&catalog%5BinitiativeId%5D=any%28962a8b7095c743e3b521ed2765ce7930%29&page%5Bkey%5D=eyJodWIiOnsic3RhcnQiOjIxLCJzaXplIjoxMH0sImFnbyI6eyJzdGFydCI6MSwic2l6ZSI6MTB9fQ%3D%3D'
response = requests.post(url)

#print(response.status_code)
#print(response.json())
response_json = response.json()
#print(response_json)



with open("sample.json") as jsonFile:
    data = json.load(jsonFile)
    jsonData = data["data"]["meta"]
    for x in jsonData:
        keys = x.keys()
        print(keys)

#while response_json['meta']['next'] in response_json:


#next_key_value = response_json['meta']['next']
#print(next_key_value)

#response = requests.post(next_key_value, json=payload)


pretty_response = json.dumps(response.json(), indent=4)
with open("sample_2.json", "w") as outfile:
    outfile.write(pretty_response)

#print(pretty_response)


#Craft a dataframe of all the datasets using the RSS feed

#Gather date updated information on a daily basis using Beautiful Soup

#if the last item on the page still has that date (more than 20 -- send a warning error that not all updates collected)
   #OR figure out how to press button using Selenium
#save the old table and new table and comapre them

#Potential for scraping:
    #RSS feed (hard to tell if updated every day, appears to have Pubb date and not updated): https://datahub-dc-dcgis.hub.arcgis.com/api/feed/rss/2.0
    #API (recommended on site for geospatial stuff): https://datahub-dc-dcgis.hub.arcgis.com/api/search/definition/#/

url = 'https://www.ola.state.md.us/Search/Report?keyword=&agencyId=&dateFrom=&dateTo='
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
html = response.content

soup = BeautifulSoup(html, features="html.parser")
table = soup.find('tbody')