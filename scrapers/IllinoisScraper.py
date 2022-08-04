from scrapers.WebsiteScraper import WebsiteScraper

import time
import requests
import os
from bs4 import BeautifulSoup
import io
import json
from os.path import exists
from datetime import datetime
from pathvalidate import sanitize_filename #not native

class IllinoisScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd() # get current dir for file pathing ,  C:\Users\chloe\Downloads\pilabsScraper-main
        headers = self._headers # Many websites prevent scraping from default clients, so provide a client header such as firefox information
        url = self._base_url # Base url being https://dph.illinois.gov
        time.sleep(5) # Scrapers must wait 5 seconds between requests else risking getting IP banned
        base_html = requests.get(self._base_url + "/topics-services/diseases-and-conditions/diseases-a-z-list.html", headers=headers).text # gets url of letter a diseases and
        # conditions, headers is so that you pretend to be a browser

        base_soup = BeautifulSoup(base_html, 'lxml') # using beautiful soup to parse html
        print('[Illinois]Retrieved base indices...') # just a check

        diseaseAndConditions = originDir + "\\DiseasesAndConditions"
        if not os.path.exists(diseaseAndConditions): # if path dne create diseases and conditions directory in originDir
            os.mkdir(diseaseAndConditions) # makes new folder

        osDir = diseaseAndConditions + "\\" + "Illinois" # if dne, create Ill directory
        if not os.path.exists(osDir):
            os.makedirs(osDir) # creates new folder as well as sub-folder (for all letters)

        letterbox = base_soup.find('ol', role="tablist").find_all('li') #container that stores the tabs for letter ranges (A-D, E-H, etc)
        i = 0 #all the columns containing the disease links are on one page, the i variable increases by 2 each time bc each tab for letter ranges has 2 columns
        for tab in letterbox: #for every <li> role='tab', which is each letter range
            letterRange = tab.get_text()
            print(letterRange)
            newPath = osDir + "\\" + letterRange.strip()
            if (not os.path.exists(newPath)):
                os.makedirs(newPath)


            column = base_soup.find_all('div', class_='cmp-text')[i].find_all('a', href=True) 
            i+=1
            column = base_soup.find_all('div', class_='cmp-text')[i].find_all('a', href=True) 
            i+=1

            for disease in column:
                try:

                    diseaseName = disease.get_text() # name of disease from html element
                    print(diseaseName)
                    if "https" in disease['href']: #some disease links are the full link to NIH
                        diseaseUrl = disease['href']
                    else:
                        diseaseUrl = url + disease['href']
            
                #     print('[ILLINOIS][LOG] Retrieving ', diseaseUrl, '...')

                    time.sleep(5)
                    html_diseases = requests.get(diseaseUrl, headers=headers) # could put .text here
                    print('[ILLINOIS]Retrieved Illinois URL ', diseaseUrl)

                except:
                    print('[ILLINOIS][LOG] Retrieval Error')
                    continue

                try:
                    diseaseSoup = BeautifulSoup(html_diseases.text, 'lxml') # soup
                except:
                    print('[ILLINOIS][LOG] Soup Error')
                    continue

                try:
                    fileName = sanitize_filename(diseaseName)
                    jsonPath = osDir + "/" + fileName + ".json"

                    date = datetime.now() # date scraped

                    data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                            "name": diseaseName,
                            "raw_html": diseaseSoup.prettify(),
                            "source_url": url,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "Illinois"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4) #store "data" as json file
                except:
                    print('[ILLINOIS][LOG] Write error')
