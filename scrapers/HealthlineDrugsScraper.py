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


class HealthlineDrugsScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()
        headers = self._headers
        base_url = self._base_url 
        time.sleep(5)
        base_html = requests.get(self._base_url, headers=headers).text
        

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[Healthline]Retrieved base indices...')
        
        osDir = originDir + "\\" + "Drugs\\" "HealthlineDrugs"
        if not os.path.exists(osDir):
                os.makedirs(osDir)
                
        drugContainer = base_soup.find('ul', class_="css-ufl5o8")
        drugs = drugContainer.find_all('a', href=True)
    
        for link in drugs:
            url =  base_url + link['href'] #Form complete url from href
            print('[Healthline]Retrieving ', link['href'], '...')
            drugName = link.get_text()
            urlToDrug = base_url + link['href']

            time.sleep(5)
            html_drugs = requests.get(urlToDrug, headers=headers).text
            print('[Healthline]Retrieved Healthline URL ', urlToDrug)

            diseaseSoup = BeautifulSoup(html_drugs, 'lxml')
            
            fileName = sanitize_filename(drugName)
            jsonPath = osDir + "/" + fileName + ".json"
                
            date = datetime.now()
            
            data = {
                    "name": drugName,
                    "raw_html": diseaseSoup.prettify(),
                    "source_url": url,
                    "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                    "source_name": "Healthline"
                }
            
            with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                json.dump(data, file, indent = 4)