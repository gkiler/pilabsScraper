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


class CDCScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()
        headers = self._headers
        base_url = 'https://www.cdc.gov'
        time.sleep(5)
        base_html = requests.get("https://www.cdc.gov/diseasesconditions/az/a.html", headers=headers).text
        

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[CDC]Retrieved base indices...')
        
        osDir = originDir + "\\" + "Diseases\\" "CDCDiseases"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        indices = base_soup.find('div', class_='col mb-3')
        indexLinks = indices.find_all('a', href=True)
        
        for indexLetters in indexLinks:
            letterName = indexLetters.text
            newpath = osDir + "\\" + letterName.strip()
            
            nextLetter = chr(ord(letterName)+1)
            testPath = osDir + "\\" + nextLetter

            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)

            get_url = base_url + indexLetters['href']
            print('[CDC]Getting URL ', get_url, '...')

            time.sleep(5)
            
            html_text = requests.get(get_url, headers=headers).text

            soup = BeautifulSoup(html_text, 'lxml')
            print("[CDC]Retrieved index...")

            diseases = soup.find('ul', class_='unstyled-list pl-0')
            webLink = diseases.find_all('a', href=True)
            
            
            for link in webLink:

                # try:
                print('[CDC]Retrieving ', link['href'], '...')
                url = link['href']
                time.sleep(5)
                html_disease = requests.get(url, headers=headers)
                # except:
                #     print('[CDC]Retrieval Error')
                #     continue
                try:
                    diseaseSoup = BeautifulSoup(html_disease.text, 'lxml')
                except:
                    print('[CDC]Soup Error')
                    continue
                    # row = letterSoup.find('div', class_='row')  # disease information
                
                    # headerToLink = row.find('h1')
                try:
                    header = link.text
                    # header = diseaseSoup.find('span', class_='mobile-title').text  # name of disease
                    print('[CDC]Retrieved ', header, ' data...')
                except:
                    print('[CDC]Header error')

                
                
                # contentInstance = letterSoup.find('div',id='main-content')  # all info on page
                    # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
                
                # try:
                #     headerLoc = header.find('/')
                #     while (headerLoc != -1):
                #         headerLoc = header.find('/')
                #         header = header.replace('/',' ')
                # except:
                #     print('[CDC]NoneType object except')
                #     continue
                try:
                    diseaseName = header
                    fileName = sanitize_filename(diseaseName)
                    jsonPath = newpath + "/" + fileName + ".json"
                        
                    date = datetime.now()
                    
                    data = {
                            "name": diseaseName,
                            "raw_html": diseaseSoup.prettify(),
                            "source_url": url,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "CDC"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4)
                    # with io.open(newpath + "\\" + header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                    #     f.write(contentInstance.prettify()) 
                except:
                    print('[CDC]Write error')