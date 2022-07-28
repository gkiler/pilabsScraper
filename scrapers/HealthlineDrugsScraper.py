from scrapers.WebsiteScraper import WebsiteScraper

import time
import requests
import os
from bs4 import BeautifulSoup
from requests_html import HTMLSession
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
        
        drugs = originDir + "\\Drugs"
        if not os.path.exists(drugs): # if path dne create diseases and conditions directory in originDir
            os.mkdir(drugs) # makes new folder
            #is this needed

        osDir = originDir + "\\" + "Drugs\\" "HealthlineDrugs"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        drugs = base_soup.findAll('a', class_='css-1hacg05')
        for drug in drugs:
            print(drug.text)
            print(f"healthline.com{drug.get('href')}")
            print()

        # drugContainer = base_soup.find_all('a', class_="css-1hacg05") #not that many drugs so can put it in one folder
        # print(drugContainer)
        # for link in drugContainer:
        #     url =  base_url + link['href'] #Form complete url from href
        #     print('[Healthline]Retrieving ', link['href'], '...')
        #     drugName = link.get_text()
        #     urlToDrug = base_url + link['href']

        #     time.sleep(5)
        #     html_drugs = requests.get(urlToDrug, headers=headers).text
        #     print('[Healthline]Retrieved Healthline URL ', urlToDrug)

        #     diseaseSoup = BeautifulSoup(html_drugs, 'lxml')
            
        #     fileName = sanitize_filename(drugName)
        #     jsonPath = osDir + "/" + fileName + ".json"
                
        #     date = datetime.now()
            
        #     data = {
        #             "name": drugName,
        #             "raw_html": diseaseSoup.prettify(),
        #             "source_url": url,
        #             "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
        #             "source_name": "Healthline"
        #         }
            
        #     with io.open(jsonPath, 'w+', encoding='utf-8') as file:
        #         json.dump(data, file, indent = 4)