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


class RIDHScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()
        headers = self._headers
        url = 'https://health.ri.gov/diseases/infectious/'
        baseUrl = 'https://health.ri.gov'
        time.sleep(5)
        base_html = requests.get("https://health.ri.gov/diseases/infectious/", headers=headers).text
        

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[RIDH]Retrieved base indices...')
        
        osDir = originDir + "\\" + "InfectiousDiseases\\" "RIDHDiseases"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        diseaseTemp = base_soup.find('div', class_='panel')
        aTag = diseaseTemp.find_all('a', href=True)
    
        for link in aTag:
            diseaseLink = link['href']
            if diseaseLink.startswith('/'):
                if diseaseLink.startswith('p', 1) or diseaseLink.startswith('a', 2):
                    continue
                diseaseName = link.get_text()
                urlToDisease = baseUrl + diseaseLink
            else:
                continue
            print('[ECDC]Retrieving ', diseaseLink, '...')

            time.sleep(5)
            html_diseases = requests.get(urlToDisease, headers=headers).text
            print('[RIDH]Retrieved RIDH URL ', urlToDisease)

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
