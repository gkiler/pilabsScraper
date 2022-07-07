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

class FamilyDoctorScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd() # get current dir for file pathing C:/payto
        headers = self._headers # Many websites prevent scraping from default clients, so provide a client header such as firefox information
        base_url = self._base_url # Base url being https://familydoctor.org
        time.sleep(5) # Scrapers must wait 5 seconds between requests else risking getting IP banned
        base_html = requests.get(self._base_url + "/diseases-and-conditions/?alpha=A", headers=headers).text # gets url of letter a diseases and
        # conditions, headers is so that you pretend to be a browser

        base_soup = BeautifulSoup(base_html, 'lxml') # using beautiful soup to parse html
        print('[FamilyDoctor]Retrieved base indices...') # ??

        diseaseAndConditions = originDir + "\\DiseasesAndConditions"
        if not os.path.exists(diseaseAndConditions): # if path dne create diseases and conditions directory in originDir
            os.mkdir(diseaseAndConditions) # makes new folder

        osDir = diseaseAndConditions + "\\" + "FamilyDoctor" # if dne, create FamilyDoctor directory
        if not os.path.exists(osDir):
            os.makedirs(osDir) # creates new folder as well as sub-folder (for all letters)

        indices = base_soup.find('div', class_='facet-container facet-alpha clearfix active') # where each letter of alphabet is contained
        indexLinks = indices.find_all('a', href=True) # retrieve all href links within container

        for letters in indexLinks: # iterate through each hyperlink
            letterName = "".join(x for x in letters.get_text() if x.isalnum()) # verify folder name can be made, remove spaces or any weird occurences (list comprehension)
            newPath = osDir + "\\" + letterName.strip() # retrieve the letter name from the html element

            nextLetter = chr(ord(letterName)+1) #Assume that if the next letter exists, this current letter has been completely scraped.
                                                    #TODO: Small error where indexes labelled "#" or "0-9" cannot be scraped as they are not alphanumeric. Add try catch statement
            testPath = osDir + "\\" + nextLetter 
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newPath)):
                os.makedirs(newPath)
                                                
            url = base_url + "/" + letters['href'] #Form complete url from href
            print('[FamilyDoctor]Retrieving FamilyDoctor URL ',url,'...') 

            time.sleep(5)#wait 5 seconds, then request
            htmlText = requests.get(url, headers=headers).text
