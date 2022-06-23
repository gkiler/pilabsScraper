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


class NHSScottishScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()
        headers = self._headers
        base_url = 'https://www.nhsinform.scot'
        time.sleep(10)
        base_html = requests.get("https://www.nhsinform.scot/illnesses-and-conditions/a-to-z#A", headers=headers).text
        

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[NHS SCOTTISH]Retrieved base indices...')
        
        osDir = originDir + "\\" + "Diseases\\" "NHSScottishDiseases"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        diseaseTemp = base_soup.find_all('div', class_='row')
        diseases = diseaseTemp[2].find_all('a', href=True)
        # print(diseases)
    
        for link in diseases:
            try:
                print('[NHS SCOTTISH]Retrieving ', link['href'], '...')
                url = base_url + link['href']

                time.sleep(10)
                html_disease = requests.get(url, headers=headers).text
                
                
            except:
                print('[NHS SCOTTISH]Retrieval Error')
                continue
            try:
                diseaseSoup = BeautifulSoup(html_disease, 'lxml')
            except:
                print('[NHS SCOTTISH]Soup Error')
                continue
                # row = letterSoup.find('div', class_='row')  # disease information
            
                # headerToLink = row.find('h1')
            try:
                header = link.text  # name of disease
                print('[NHS SCOTTISH]Retrieved ', header, ' data...')
            except:
                print('[NHS SCOTTISH]Header error')

            
            
            # contentInstance = letterSoup.find('div',id='main-content')  # all info on page
                # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
            
            # try:
            #     headerLoc = header.find('/')
            #     while (headerLoc != -1):
            #         headerLoc = header.find('/')
            #         header = header.replace('/',' ')
            # except:
            #     print('[NHS SCOTTISH]NoneType object except')
            #     continue
            try:
                diseaseName = header
                fileName = sanitize_filename(diseaseName)
                jsonPath = osDir + "/" + fileName + ".json"
                    
                date = datetime.now()
                
                data = {
                        "name": diseaseName,
                        "raw_html": diseaseSoup.prettify(),
                        "source_url": url,
                        "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                        "source_name": "NHSScottish"
                    }
                
                with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                    json.dump(data, file, indent = 4)
                # with io.open(newpath + "\\" + header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                #     f.write(contentInstance.prettify()) 
            except:
                print('[NHS SCOTTISH]Write error')