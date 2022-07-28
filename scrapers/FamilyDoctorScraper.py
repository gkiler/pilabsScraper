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
        base_html = requests.get(self._base_url + "/diseases-and-conditions/", headers=headers).text # gets url of letter a diseases and
        # conditions, headers is so that you pretend to be a browser

        base_soup = BeautifulSoup(base_html, 'lxml') # using beautiful soup to parse html
        print('[FamilyDoctor]Retrieved base indices...') # just a check

        diseaseAndConditions = originDir + "\\DiseasesAndConditions"
        if not os.path.exists(diseaseAndConditions): # if path dne create diseases and conditions directory in originDir
            os.mkdir(diseaseAndConditions) # makes new folder

        osDir = diseaseAndConditions + "\\" + "FamilyDoctor" # if dne, create FamilyDoctor directory
        if not os.path.exists(osDir):
            os.makedirs(osDir) # creates new folder as well as sub-folder (for all letters)

        indices = base_soup.find('div', class_='facet-container facet-alpha clearfix') # where each letter of alphabet is contained
        indexLinks = indices.find_all('a', href=True) # retrieve all href links within container

        for letters in indexLinks: # iterate through each hyperlink
            letterName = "".join(x for x in letters.get_text() if x.isalnum()) # verify folder name can be made, remove spaces or any weird occurences (list comprehension)
            newPath = osDir + "\\" + letterName.strip() # retrieve the letter name from the html element
            
            print(letterName)
            
            nextLetter = chr(ord(letterName)+1) #Assume that if the next letter exists, this current letter has been completely scraped.
                                                    #TODO: Small error where indexes labelled "#" or "0-9" cannot be scraped as they are not alphanumeric. Add try catch statement
            testPath = osDir + "\\" + nextLetter 
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newPath)):
                os.makedirs(newPath)
                                                
            url = letters['href'] #Form complete url from href
            print('[FamilyDoctor]Retrieving FamilyDoctor URL ',url,'...')

            time.sleep(5) # wait 5 seconds, then request
            htmlText = requests.get(url, headers=headers).text

            soup = BeautifulSoup(htmlText, 'lxml')
            print("[LOG] Retrieved index...")

            # while loop for 'next page' button
            while True: 
                time.sleep(5)

                htmlText = requests.get(url, headers=headers).text
                soup = BeautifulSoup(htmlText, 'lxml')

                diseases = soup.find('div', class_='search-results clearfix')
                aTag = diseases.find_all('a', href=True, attrs={"class" : "link-to-post"})

                for link in aTag:
                    diseaseName = link.get_text() # name of disease from html element
                    diseaseUrl = link['href']
            
                    print('[FAMILYDOC][LOG] Retrieving ', diseaseUrl, '...')

                    time.sleep(5)
                    html_diseases = requests.get(diseaseUrl, headers=headers) # could put .text here
                    print('[FAMILYDOCTOR]Retrieved FamilyDoc URL ', diseaseUrl)

                    diseaseSoup = BeautifulSoup(html_diseases.text, 'lxml') # soup

                    fileName = sanitize_filename(diseaseName)
                    jsonPath = newPath + "/" + fileName + ".json"

                    date = datetime.now() # date scraped

                    data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                            "name": diseaseName,
                            "raw_html": diseaseSoup.prettify(),
                            "source_url": diseaseUrl,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "Family Doctor"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4) #store "data" as json file

                # how to go to the next page
                next_page_url = soup.find('li', attrs={"class": "next"})
                
                # print(next_page_url)
                if next_page_url:
                    next_page_url = next_page_url.find("a", href=True)
                    url = next_page_url['href']
                    print(url)
                else:
                    break