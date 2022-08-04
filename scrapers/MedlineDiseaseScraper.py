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

class MedlineDiseaseScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd() # get current dir for file pathing 
        headers = self._headers # Many websites prevent scraping from default clients, so provide a client header such as firefox information
        base_url = self._base_url 
        time.sleep(5) # Scrapers must wait 5 seconds between requests else risking getting IP banned
        base_html = requests.get(self._base_url + "encyclopedia_A.htm", headers=headers).text # gets url of letter a diseases and
        # conditions, headers is so that you pretend to be a browser

        base_soup = BeautifulSoup(base_html, 'lxml') # using beautiful soup to parse html
        print('[Medline]Retrieved base indices...') 

        diseaseAndConditions = originDir + "\\DiseasesAndConditions"
        if not os.path.exists(diseaseAndConditions): # if path dne create diseases and conditions directory in originDir
            os.mkdir(diseaseAndConditions) # makes new folder

        osDir = diseaseAndConditions + "\\" + "Medline Diseases" # if dne, create MD directory
        if not os.path.exists(osDir):
            os.makedirs(osDir) # creates new folder as well as sub-folder (for all letters)

        newPath = osDir + "\\" + 'A' # retrieve the letter name from the html element
            
        print('A')
                                            
        url = "https://medlineplus.gov/ency/encyclopedia_A.htm"
        print('[Medline]Retrieving Medline URL ',url,'...')

        time.sleep(5) # wait 5 seconds, then request
        htmlText = requests.get(url, headers=headers).text

        soup = BeautifulSoup(htmlText, 'lxml')
        print("[LOG] Retrieved index...")

        #loop thru every link for letter A
        diseases = soup.find('ul', id="index")
        aTag = diseases.find_all('a', href=True) #go thru every link for a letter

        for link in aTag:
            diseaseName = link.get_text() # name of disease from html element
            # if 'for' or '?' or 'A ' or 'scan' or 'pain' or '' or '' in diseaseName:
            #     continue
            testPath = osDir + "\\" + 'B' 
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newPath)):
                os.makedirs(newPath)
                
            diseaseUrl = base_url + link['href']
    
            print('[Medline][LOG] Retrieving ', diseaseUrl, '...')

            time.sleep(5)
            html_diseases = requests.get(diseaseUrl, headers=headers) # could put .text here
            print('[Medline]Retrieved Medline URL ', diseaseUrl)

            diseaseSoup = BeautifulSoup(html_diseases.text, 'lxml') # soup

            fileName = sanitize_filename(diseaseName)
            jsonPath = newPath + "/" + fileName + ".json"

            date = datetime.now() # date scraped

            data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                    "name": diseaseName,
                    "raw_html": diseaseSoup.prettify(),
                    "source_url": url,
                    "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                    "source_name": "Medline Encyclopedia"
                }
            
            with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                json.dump(data, file, indent = 4) #store "data" as json file
                    
        indices = base_soup.find('ul', class_='alpha-links') # where each letter of alphabet is contained
        indexLinks = indices.find_all('a', href=True) # retrieve all href links within container

        for letters in indexLinks: # iterate through each hyperlink
            if len(letters.get_text())==1:
                letterName = "".join(x for x in letters.get_text() if x.isalnum()) # verify folder name can be made, remove spaces or any weird occurences (list comprehension)
                newPath = osDir + "\\" + letterName.strip() # retrieve the letter name from the html element                    
                print(letterName)          
                nextLetter = chr(ord(letterName)+1) #Assume that if the next letter exists, this current letter has been completely scraped.
            else:
                newPath = osDir + "\\" + letters.get_text() # retrieve the letter name from the html element                    
                
            testPath = osDir + "\\" + nextLetter 
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newPath)):
                os.makedirs(newPath)
                                                
            url = base_url + letters['href'] #Form complete url from href
            print('[Medline]Retrieving Medline URL ',url,'...')

            time.sleep(5) # wait 5 seconds, then request
            htmlText = requests.get(url, headers=headers).text

            soup = BeautifulSoup(htmlText, 'lxml')
            print("[LOG] Retrieved index...")
    
            diseases = soup.find('ul', id='index')
            aTag = diseases.find_all('a', href=True) #the first letter, A, does not have an href link

            for link in aTag:
                diseaseName = link.get_text() # name of disease from html element
                # if 'for' or '?' or 'A ' or 'scan' or 'pain' or '' or '' in diseaseName:
                #     continue
                diseaseUrl = base_url + link['href']
        
                print('[Medline][LOG] Retrieving ', diseaseUrl, '...')

                time.sleep(5)
                html_diseases = requests.get(diseaseUrl, headers=headers) # could put .text here
                print('[Medline]Retrieved Medline URL ', diseaseUrl)

                diseaseSoup = BeautifulSoup(html_diseases.text, 'lxml') # soup

                fileName = sanitize_filename(diseaseName)
                jsonPath = newPath + "/" + fileName + ".json"

                date = datetime.now() # date scraped

                data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                        "name": diseaseName,
                        "raw_html": diseaseSoup.prettify(),
                        "source_url": url,
                        "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                        "source_name": "Medline Encyclopedia"
                    }
                
                with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                    json.dump(data, file, indent = 4) #store "data" as json file

            