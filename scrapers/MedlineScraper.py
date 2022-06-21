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


class MedlineScraper(WebsiteScraper):
    def scrape(self):
        headers = self._headers

        originDir = os.getcwd()

        base_url = self._base_url
        base_url2 = base_url + "/" + 'druginfo'
        time.sleep(5)
        base_html = requests.get(base_url + "/druginformation.html", headers=headers)

        base_soup = BeautifulSoup(base_html.text, 'lxml')
        print(f'[LOG] Retrieved base indices...')

        osDir = originDir + "\\" + "Drugs\\" "medlineDrugs"
        if not os.path.exists(osDir):
            os.makedirs(osDir)

        indices = base_soup.find('ul', class_='alpha-links')
        indexLinks = indices.find_all('a', href=True)
        
        for indexLetters in indexLinks:
            letterName = indexLetters.get_text()
            newpath = osDir + "\\" + letterName
            
            nextLetter = chr(ord(letterName)+1)
            testPath = osDir + "\\" + nextLetter

            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)

            # os.chdir(newpath)

            get_url = base_url + "/" + indexLetters['href']
            print('[LOG] Getting URL ', get_url, '...')

            time.sleep(5)
            
            html_text = requests.get(get_url, headers=headers).text

            soup = BeautifulSoup(html_text, 'lxml')
            print("[LOG] Retrieved index...")

            drugs = soup.find('ul',id="index")
            webLink = drugs.find_all('a', href=True)
            
            for link in webLink:

                try:
                    tempLink = link['href'][2 : : ]
                    url = base_url2 + "/" + tempLink
                    print('[LOG] Retrieving ', url, '...')

                    time.sleep(5)
                    html_drugs = requests.get(url, headers=headers).text
                    
                    
                except:
                    print('[LOG] Retrieval Error')
                    continue
                try:
                    drugSoup = BeautifulSoup(html_drugs, 'lxml')
                except:
                    print('[LOG] Soup Error')
                    continue
                try:
                    header = drugSoup.find('h1').text # name of disease
                    print('[LOG] Retrieved ', header, ' data...')
                except:
                    print('[LOG] Header error')
                
                # contentInstance = letterSoup.find('div',id='mplus-content')  # all info on page
                
                try:
                    headerLoc = header.find('/')
                    while (headerLoc != -1):
                        headerLoc = header.find('/')
                        header = header.replace('/',' ')
                except:
                    print('[LOG] NoneType object except')
                    continue
                try:
                    drugName = header
                    fileName = sanitize_filename(drugName)
                    jsonPath = newpath + "/" + fileName + ".json"
                        
                    date = datetime.now()
                    
                    data = {
                            "name": drugName,
                            "raw_html": drugSoup.prettify(),
                            "source_url": url,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "Medline"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4)
                    # with io.open(newpath + "\\" + header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                    #     f.write(contentInstance.prettify()) 
                except:
                    print('[LOG] Write error')