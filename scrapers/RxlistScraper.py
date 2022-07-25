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

class RxlistScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd() # get current dir for file pathing C:/payto
        headers = self._headers # Many websites prevent scraping from default clients, so provide a client header such as firefox information
        base_url = self._base_url # Base url being https://familydoctor.org
        time.sleep(5) # Scrapers must wait 5 seconds between requests else risking getting IP banned
        base_html = requests.get("https://www.rxlist.com/drugs/alpha_a.htm", headers=headers).text # gets url of letter a diseases and
        # conditions, headers is so that you pretend to be a browser

        base_soup = BeautifulSoup(base_html, 'lxml') # using beautiful soup to parse html
        print('[Rxlist]Retrieved base indices...') # just a check

        drugs = originDir + "\\Drugs"
        if not os.path.exists(drugs): # if path dne create diseases and conditions directory in originDir
            os.mkdir(drugs) # makes new folder

        osDir = drugs + "\\" + "Rxlist" # if dne, create FamilyDoctor directory
        if not os.path.exists(osDir):
            os.makedirs(osDir) # creates new folder as well as sub-folder (for all letters)

        letterContainer = base_soup.find('div', id='A_Z')
        aTagContainer = letterContainer.find_all('a', href=True)

        for aTagLetters in aTagContainer: # iterate through each hyperlink
            letterName = "".join(x for x in aTagLetters.get_text() if x.isalnum()) # verify folder name can be made, remove spaces or any weird occurences (list comprehension)
            newPath = osDir + "\\" + letterName.strip() # retrieve the letter name from the html element
            
            print(letterName)
            
            nextLetter = chr(ord(letterName)+1) #Assume that if the next letter exists, this current letter has been completely scraped.
                                                    #TODO: Small error where indexes labelled "#" or "0-9" cannot be scraped as they are not alphanumeric. Add try catch statement
            testPath = osDir + "\\" + nextLetter 
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newPath)):
                os.makedirs(newPath)
                                                
            url = base_url + aTagLetters['href'] #Form complete url from href
            print('[Rxlist]Retrieving Rxlist letter URL ',url,'...')

            time.sleep(5) # wait 5 seconds, then request
            htmlText = requests.get(url, headers=headers).text
            soup = BeautifulSoup(htmlText, 'lxml')
            print("[LOG] Retrieved index...")

            drugContainer = soup.find('div', class_='AZ_results')
            aTagContainer = drugContainer.find_all('a', href=True)

            for aTagDrugs in aTagContainer:

                drugName = aTagDrugs.get_text() # name of disease from html element
                drugUrl = aTagDrugs['href']

                if drugUrl.startswith('#'):
                    continue
                print('[RXLIST][LOG] Retrieving ', drugUrl, '...')

                time.sleep(5)
                htmlDrugs = requests.get(drugUrl, headers=headers).text # could put .text here
                print('[RXLIST]Retrieved Rxlist URL ', drugUrl)

                drugSoup = BeautifulSoup(htmlDrugs, 'lxml') # soup

                try:
                    fileName = sanitize_filename(drugName)
                    jsonPath = newPath + "/" + fileName + ".json"

                    date = datetime.now() # date scraped

                    data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                            "name": drugName,
                            "raw_html": drugSoup.prettify(),
                            "source_url": url,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "Rxlist"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4) #store "data" as json file
                except:
                        print("[RXLIST] Write Error")