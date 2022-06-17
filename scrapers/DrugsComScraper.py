from scrapers.WebsiteScraper import WebsiteScraper

import time
import requests
import os
from bs4 import BeautifulSoup
import io
import json
from os.path import exists
from datetime import datetime

class DrugsComScraper(WebsiteScraper):
    def scrape(self):
        indexCount = 0

        originDir = os.getcwd()

        base_url = self._base_url

        time.sleep(5)
        base_html = requests.get(base_url + "/".join(self._ext)).text

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('Retrieved base indices...')
        
        if not os.path.exists(originDir + "\\Drugs"):
            os.mkdir(originDir + "\\Drugs")
        # drugsPath = originDir + "\\Drugs"
        osDir = originDir + "\\" + "Drugs\\" "drugsCom"
        if not os.path.exists(osDir):
                os.mkdir(osDir)

       


        indices = base_soup.find('nav', class_='ddc-paging')
        indexLinks = indices.find_all('a',href=True)

        for letters in indexLinks:
            letterName = letters.get_text()
            newpath = osDir + "\\" + letterName

            #add redundancy detections
            if not os.path.exists(newpath):
                os.mkdir(newpath)

            url = base_url + letters['href']
            print('Retrieving Drugs.com URL ',url,'...')

            time.sleep(5)
            htmlText = requests.get(url).text

            soup = BeautifulSoup(htmlText,'lxml')
            print('Retrieved Drugs.com URL ',url)

            subIndices = soup.find('nav', class_='ddc-paging paging-list-wrap ddc-mgb-2')
            subIndexLinks = subIndices.find_all('a',href=True)

            for subLetter in subIndexLinks:
                print('Retrieving Drugs.com URL ', base_url + subLetter['href'],'...')
                time.sleep(5)
                subHtmlText = requests.get(base_url + subLetter['href'])
                print('Retrieved Drugs.com URL ', base_url + subLetter['href'])
                subDrugSoup = BeautifulSoup(subHtmlText.text,'lxml')

                subDrug = subDrugSoup.find('ul', class_='ddc-list-column-2')
                subDrugList = subDrug.find_all('a', href=True)
                
                for drug in subDrugList:
                    ++indexCount

                    drugName = drug.get_text()
                    drugUrl = base_url + drug['href']

                    print('Retrieving Drugs.com URL ', drugUrl,'...')
                    time.sleep(5)
                    drugHtml = requests.get(drugUrl)
                    print('Retrieved Drugs.com URL ', drugUrl)
                    
                    drugSoup = BeautifulSoup(drugHtml.text,'lxml')
                    # drugInfo = drugSoup.find('div',class_='contentBox')

                    #fix file name errors
                    errorLoc = drugName.find('/')
                    while (errorLoc != -1):
                        drugName = drugName.replace('/',' ')
                        errorLoc = drugName.find('/')
                    
             
                    jsonPath = newpath + "/" + drugName + ".json"
                        
                    date = datetime.now()
                    title = drugSoup.find("title").getText()
                    
                    data = {
                            "name": drugName,
                            "raw_html": drugSoup.prettify(),
                            "source_url": drugUrl,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": title,
                            "index": indexCount                     
                    }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4)
                    

                    #deprecated
                    # with io.open(newpath + "/" + drugName+'.txt','w',encoding='utf-8') as f:
                    #     f.write(drugInfo.prettify())