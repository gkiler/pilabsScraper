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


class ECDCScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()
        headers = self._headers
        url = 'https://www.ecdc.europa.eu/en/all-topics'
        base_url = 'https://www.ecdc.europa.eu' # had to take out /en bc it was included in the href links for the different diseases
        time.sleep(5)
        base_html = requests.get("https://www.ecdc.europa.eu/en/all-topics", headers=headers).text
        

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[ECDC]Retrieved base indices...')
        
        osDir = originDir + "\\" + "Diseases\\" "ECDCDiseases"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        diseaseTemp = base_soup.find('ul', class_='disease-overview')
        diseases = diseaseTemp.find_all('a', href=True)
        # print(diseases)
    
        for link in diseases:
            print('[ECDC]Retrieving ', link['href'], '...')
            diseaseName = link.get_text()
            urlToDisease = base_url + link['href']

            time.sleep(5)
            html_diseases = requests.get(urlToDisease, headers=headers).text
            print('[ECDC]Retrieved ECDC URL ', urlToDisease)

            diseaseSoup = BeautifulSoup(html_diseases, 'lxml')
            
            fileName = sanitize_filename(diseaseName)
            jsonPath = osDir + "/" + fileName + ".json"
                
            date = datetime.now()
            
            data = {
                    "name": diseaseName,
                    "raw_html": diseaseSoup.prettify(),
                    "source_url": url,
                    "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                    "source_name": "ECDC"
                }
            
            with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                json.dump(data, file, indent = 4)
