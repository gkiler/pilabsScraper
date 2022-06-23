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


class MayoclinicScraper(WebsiteScraper):
    def scrape(self):
        self.parse_diseases()


        originDir = os.getcwd()
        headers = self._headers
        base_url = 'https://www.mayoclinic.org'
        time.sleep(5)
        base_html = requests.get("https://www.mayoclinic.org/drugs-supplements/drug-list", headers=headers).text
        

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[MAYOCLINIC]Retrieved base indices...')
        
        osDir = originDir + "\\" + "Drugs\\" "mayoclinicDrugs"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        indices = base_soup.find('ol', class_='acces-alpha')
        indexLinks = indices.find_all('a', href=True)
        
        for indexLetters in indexLinks:
            letterName = indexLetters.select('span')[1].get_text()
            newpath = osDir + "\\" + letterName.strip()
            
            nextLetter = chr(ord(letterName)+1)
            testPath = osDir + "\\" + nextLetter

            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)

            get_url = base_url + indexLetters['href']
            print('[MAYOCLINIC]Getting URL ', get_url, '...')

            time.sleep(5)
            
            html_text = requests.get(get_url, headers=headers).text

            soup = BeautifulSoup(html_text, 'lxml')
            print("Retrieved index...")

            diseases = soup.find('div', class_='index content-within', id='index')
            webLink = diseases.find_all('a', href=True)
            
            
            for link in webLink:

                try:
                    print('[MAYOCLINIC]Retrieving ', link['href'], '...')
                    url = base_url + link['href']

                    time.sleep(5)
                    html_disease = requests.get(url, headers=headers).text
                    
                    
                except:
                    print('[MAYOCLINIC]Retrieval Error')
                    continue
                try:
                    drugSoup = BeautifulSoup(html_disease, 'lxml')
                except:
                    print('[MAYOCLINIC]Soup Error')
                    continue
                    # row = letterSoup.find('div', class_='row')  # disease information
                
                    # headerToLink = row.find('h1')
                try:
                    header = drugSoup.find('h1').find('a', href=link['href']).text  # name of disease
                    print('[MAYOCLINIC]Retrieved ', header, ' data...')
                except:
                    print('[MAYOCLINIC]Header error')

                
                
                # contentInstance = letterSoup.find('div',id='main-content')  # all info on page
                    # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
                
                # try:
                #     headerLoc = header.find('/')
                #     while (headerLoc != -1):
                #         headerLoc = header.find('/')
                #         header = header.replace('/',' ')
                # except:
                #     print('NoneType object except')
                #     continue
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
                            "source_name": "Mayoclinic"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4)
                    # with io.open(newpath + "\\" + header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                    #     f.write(contentInstance.prettify()) 
                except:
                    print('Write error')


    def parse_diseases(self):
        originDir = os.getcwd()
        headers = self._headers
        base_url = 'https://www.mayoclinic.org'
        time.sleep(5)
        base_html = requests.get("https://www.mayoclinic.org/diseases-conditions/index?letter=A", headers=headers).text
        

        base_soup = BeautifulSoup(base_html, 'lxml')
        print('[MAYOCLINIC]Retrieved base indices...')
        
        osDir = originDir + "\\" + "Diseases\\" "mayoclinicDiseases"
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        indices = base_soup.find('ol', class_='acces-alpha')
        indexLinks = indices.find_all('a', href=True)
        
        for indexLetters in indexLinks:
            letterName = indexLetters.select('span')[1].get_text()
            newpath = osDir + "\\" + letterName.strip()
            
            nextLetter = chr(ord(letterName)+1)
            testPath = osDir + "\\" + nextLetter

            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)

            get_url = base_url + indexLetters['href']
            print('[MAYOCLINIC]Getting URL ', get_url, '...')

            time.sleep(5)
            
            html_text = requests.get(get_url, headers=headers).text

            soup = BeautifulSoup(html_text, 'lxml')
            print("Retrieved index...")

            diseases = soup.find('div', class_='index content-within', id='index')
            webLink = diseases.find_all('a', href=True)
            
            
            for link in webLink:

                try:
                    print('[MAYOCLINIC]Retrieving ', link['href'], '...')
                    url = base_url + link['href']

                    time.sleep(5)
                    html_disease = requests.get(url, headers=headers).text
                    
                    
                except:
                    print('[MAYOCLINIC]Retrieval Error')
                    continue
                try:
                    diseaseSoup = BeautifulSoup(html_disease, 'lxml')
                except:
                    print('[MAYOCLINIC]Soup Error')
                    continue
                    # row = letterSoup.find('div', class_='row')  # disease information
                
                    # headerToLink = row.find('h1')
                try:
                    header = diseaseSoup.find('h1').find('a', href=link['href']).text  # name of disease
                    print('[MAYOCLINIC]Retrieved ', header, ' data...')
                except:
                    print('[MAYOCLINIC]Header error')

                
                
                # contentInstance = letterSoup.find('div',id='main-content')  # all info on page
                    # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
                
                # try:
                #     headerLoc = header.find('/')
                #     while (headerLoc != -1):
                #         headerLoc = header.find('/')
                #         header = header.replace('/',' ')
                # except:
                #     print('[MAYOCLINIC]NoneType object except')
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
                            "source_name": "Mayoclinic"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4)
                    # with io.open(newpath + "\\" + header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                    #     f.write(contentInstance.prettify()) 
                except:
                    print('[MAYOCLINIC]Write error')