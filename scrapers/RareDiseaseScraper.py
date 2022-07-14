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


class RareDiseaseScraper(WebsiteScraper):
    def scrape(self):
        headers = self._headers

        originDir = os.getcwd()

        base_url = self._base_url
        base_url2 = base_url + "/" + 'druginfo'
        time.sleep(5)
        base_html = requests.get(base_url + "/for-patients-and-families/information-resources/rare-disease-information/", headers=headers)

        base_soup = BeautifulSoup(base_html.text, 'lxml')
        print(f'[LOG] Retrieved base indices...')

        diseasePath = originDir + "\\Disease"
        if not os.path.exists(diseasePath): #if not exists, create disease directory in originDir
            os.mkdir(diseasePath)

        osDir = diseasePath + "\\"  + "RareDisease" #if not exists, create RD directory
        if not os.path.exists(osDir):
            os.makedirs(osDir) # creates new folder as well as sub-folder (for all letters)


        indices = base_soup.find('div', class_='search-alphabet')
        indexLinks = indices.find_all('a', href=True)
        
        for indexLetters in indexLinks:
            letterName = indexLetters.get_text()
            newpath = osDir + "\\" + letterName
            
            if len(letterName)>1:
                nextLetter = 'A'
                print(nextLetter)

            else:
                nextLetter = chr(ord(letterName)+1) #this website has 3 numbers, so checking next char in ascii table wont work
                print(nextLetter)

            testPath = osDir + "\\" + nextLetter
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)

            get_url = indexLetters['href']
            print('[RD][LOG] Getting URL ', get_url, '...')

            time.sleep(5)
            
            html_text = requests.get(get_url, headers=headers).text

            soup = BeautifulSoup(html_text, 'lxml')
            print("[LOG] Retrieved index...")

            diseases = soup.find('div', class_='col-lg-8 col-md-8 col-sm-8 col-xs-12')   
            column = diseases.find_all('article') #this website has all the links in one column, including the letter links, so I need to specify "article" which is the container for each indiv disease

            for block in column: #getting the link for each disease under a letter
                link=block.find('a', href= True)
                print(link)

                diseaseName = link.get_text() # name of disease from html element
                print(diseaseName)
                diseaseUrl = link['href']
        
                print('[RARE DISEASE][LOG] Retrieving ', diseaseUrl, '...')

                time.sleep(5)
                html_diseases = requests.get(diseaseUrl, headers=headers) # could put .text here
                print('[RARE DISEASE]Retrieved FamilyDoc URL ', diseaseUrl)

                diseaseSoup = BeautifulSoup(html_diseases.text, 'lxml') # soup

                fileName = sanitize_filename(diseaseName)
                jsonPath = newpath + "/" + fileName + ".json"

                date = datetime.now() # date scraped

                data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                        "name": diseaseName,
                        "raw_html": diseaseSoup.prettify(),
                        "source_url": diseaseUrl,
                        "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                        "source_name": "Rare Disease"
                    }
                
                with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                    json.dump(data, file, indent = 4) #store "data" as json file
