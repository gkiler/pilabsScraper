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

class DrugsComScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()

        base_url = self._base_url

        time.sleep(5)
        base_html = requests.get(base_url + "/".join(self._ext)).text

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[DRUGS.COM]Retrieved base indices...')
        
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
            ##########################################
            nextLetter = chr(ord(letterName)+1)
            testPath = osDir + "\\" + nextLetter

            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)#################

            #add redundancy detections
            if not os.path.exists(newpath):
                os.mkdir(newpath)

            url = base_url + letters['href']
            print('[DRUGS.COM]Retrieving Drugs.com URL ',url,'...')

            time.sleep(5)
            htmlText = requests.get(url).text#get the html to parse with beautifulsoup
        
            soup = BeautifulSoup(htmlText,'lxml')
            print('[DRUGS.COM]Retrieved Drugs.com URL ',url)

            subIndices = soup.find('nav', class_='ddc-paging paging-list-wrap ddc-mgb-2')#find index list of hrefs
            
            subIndexLinks = subIndices.find_all('a',href=True)

            
            for subLetter in subIndexLinks:
                print('[DRUGS.COM]Retrieving Drugs.com URL ', base_url + subLetter['href'],'...')
                time.sleep(5)
                subHtmlText = requests.get(base_url + subLetter['href'])
                print('[DRUGS.COM]Retrieved Drugs.com URL ', base_url + subLetter['href'])
                subDrugSoup = BeautifulSoup(subHtmlText.text,'lxml')

                subDrug = subDrugSoup.find('ul', class_='ddc-list-column-2')
                if subDrug == None:
                    subDrug = subDrugSoup.find_all('ul',class_="ddc-list-unstyled")[1]
                try:
                    subDrugList = subDrug.find_all('a', href=True)
                except:
                    continue
                # for item in subDrugList:
                #     print(item['href'])

                for drug in subDrugList:

                    drugName = drug.get_text()
                    drugUrl = base_url + drug['href']

                    print('[DRUGS.COM]Retrieving Drugs.com URL ', drugUrl,'...')
                    time.sleep(5)
                    drugHtml = requests.get(drugUrl)
                    print('[DRUGS.COM]Retrieved Drugs.com URL ', drugUrl)
                    
                    drugSoup = BeautifulSoup(drugHtml.text,'lxml')
                    # drugInfo = drugSoup.find('div',class_='contentBox')

                    #fix file name errors
                    # errorLoc = drugName.find('/')
                    # while (errorLoc != -1):
                    #     drugName = drugName.replace('/',' ')
                    #     errorLoc = drugName.find('/')
                    

                    # fileName = "".join(x for x in drugName if x.isalnum()) #only alphanumeric
                    fileName = sanitize_filename(drugName)
                    jsonPath = newpath + "/" + fileName + ".json"
                        
                    date = datetime.now()
                    
                    data = {
                            "name": drugName,
                            "raw_html": drugSoup.prettify(),
                            "source_url": drugUrl,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "Drugs.com"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4)
                    

                    #deprecated
                    # with io.open(newpath + "/" + drugName+'.txt','w',encoding='utf-8') as f:
                    #     f.write(drugInfo.prettify())