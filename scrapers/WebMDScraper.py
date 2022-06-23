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


class WebMDScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd() 
        headers = self._headers
        base_url = self._base_url
        time.sleep(5)
        base_html = requests.get(self._base_url + "/drugs/2/alpha/a", headers=headers).text

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[WEBMD]Retrieved base indices...')

        if not os.path.exists(originDir + "\\Drugs"):
            os.mkdir(originDir + "\\Drugs")
        drugsPath = originDir + "\\Drugs"

        osDir = originDir + "\\" + "Drugs\\" + "WebMD"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        indices = base_soup.find('div', class_='alpha-container')
        indexLinks = indices.find_all('a',href=True)

        for letters in indexLinks:
            letterName = "".join(x for x in letters.get_text() if x.isalnum())
            newpath = osDir + "\\" + letterName.strip()

            
            #add redundancy detections
            nextLetter = chr(ord(letterName)+1)
            testPath = osDir + "\\" + nextLetter
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)
            
            url = base_url + "/" + letters['href']
            print('[WEBMD]Retrieving WebMD URL ',url,'...')

            time.sleep(5)
            htmlText = requests.get(url, headers=headers).text

            soup = BeautifulSoup(htmlText,'lxml')
            print('[WEBMD]Retrieved WebMD URL ',url)

            subIndices = soup.find('ul',class_='browse-letters squares sub-alpha')
            subIndexLinks = subIndices.find_all('a',href=True)

            for subLetter in subIndexLinks:
                print('[WEBMD]Retrieving WebMD URL ', base_url + "/" + subLetter['href'],'...')
                time.sleep(5)
                subHtmlText = requests.get(base_url + subLetter['href'], headers=headers)
                print('[WEBMD]Retrieved WebMD URL ', base_url + subLetter['href'])
                subDrugSoup = BeautifulSoup(subHtmlText.text,'lxml')

                try:
                    subDrug = subDrugSoup.find('div',class_='drugs-search-list-conditions')
                    subDrugList = subDrug.find_all('a',href=True)
                except:
                    continue
                for drug in subDrugList:
                    drugName = drug.get_text()
                    drugUrl = base_url + "/" + drug['href']

                    print('[WEBMD]Retrieving WebMD URL ', drugUrl,'...')
                    time.sleep(5)
                    drugHtml = requests.get(drugUrl, headers=headers)
                    print('[WEBMD]Retrieved WebMD URL ', drugUrl)
                    
                    drugSoup = BeautifulSoup(drugHtml.text,'lxml')
                    # drugInfo = drugSoup.find('div',class_='pane webmd-row')

                    #fix file name errors
                    fileName = sanitize_filename(drugName)
                    jsonPath = newpath + "/" + fileName + ".json"                    # errorLoc = drugName.find('/')
                    
                                        
                    date = datetime.now()
                    
                    data = {
                            "name": drugName,
                            "raw_html": drugSoup.prettify(),
                            "source_url": url,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "WebMD"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4)
                    # with io.open(newpath + "\\" + drugName + '.txt','w',encoding='utf-8') as f:
                    #     f.write(drugInfo.prettify())