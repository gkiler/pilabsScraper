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


class HonDossierScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()
        headers = self._headers
        url = 'https://www.hon.ch/HONselect/RareDiseases/index.html'
        baseUrl = 'https://www.hon.ch'
        time.sleep(5)
        htmlText = requests.get(url, headers=headers).text
        soup = BeautifulSoup(htmlText, 'lxml')
        print('[HON]Retrieved base indices...')
        
        osDir = originDir + "\\" + "Rare Diseases\\" "Hon Dossier Diseases"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        aTagContainer = soup.find_all('a', class_='menu', href=True)
        # aTag = diseaseTemp.find_all('a', href=True)
    
        for aTagDiseases in aTagContainer:
            testUrl = aTagDiseases['href']
            if testUrl.startswith('C', 24):
                diseaseName = aTagDiseases.get_text()
                diseaseUrl = baseUrl + testUrl
            else:
                continue

            print('[HON] Disease name: ', diseaseName)

            time.sleep(5)
            html = requests.get(diseaseUrl, headers=headers).text
            soupTwo = BeautifulSoup(html, 'lxml')

            container = soupTwo.find('th')
            aTag = container.find_all('a', class_='menu', href=True)

            for tag in aTag:
                tUrl = tag['href']
                url = baseUrl + tUrl
                print('[HON]Retrieving ', url, '...')


            htmlDisease = requests.get(url, headers=headers).text
            diseaseSoup = BeautifulSoup(htmlDisease, 'lxml')
            
            fileName = sanitize_filename(diseaseName)
            jsonPath = osDir + "/" + fileName + ".json"
                
            date = datetime.now()
            
            data = {
                    "name": diseaseName,
                    "raw_html": diseaseSoup.prettify(),
                    "source_url": url,
                    "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                    "source_name": "Hon Dossier"
                }
            
            with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                json.dump(data, file, indent = 4)
