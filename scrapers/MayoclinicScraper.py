from scrapers.WebsiteScraper import WebsiteScraper

import time
import requests
import os
from bs4 import BeautifulSoup
import io

class MayoclinicScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd()

        base_url = self._base_url
        fin_url = base_url + "/".join(self._ext)

        time.sleep(5)
        base_html = requests.get(fin_url).text
        
        base_soup = BeautifulSoup(base_html, 'lxml')
        self.verboseprint(f'[LOG] Retrieved base indices...')
        
        osDir = originDir + "\\" + "Drugs\\" "mayoclinicDrugs"
        if not os.path.exists(osDir):
            os.mkdir(osDir)

        indices = base_soup.find('ol', class_='acces-alpha')
        indexLinks = indices.find_all('a', href=True)
        
        for indexLetters in indexLinks:
            letterName = indexLetters.select('span')[1].get_text()
            newpath = osDir + "\\" + letterName
            
            nextLetter = chr(ord(letterName)+1)
            testPath = osDir + "\\" + nextLetter

            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.mkdir(newpath)

            os.chdir(newpath)

            get_url = base_url + indexLetters['href']
            self.verboseprint('[LOG] Getting URL ', get_url, '...')

            time.sleep(5)
            
            html_text = requests.get(get_url).text

            soup = BeautifulSoup(html_text, 'lxml')
            self.verboseprint("[LOG] Retrieved index...")

            diseases = soup.find('div', class_='index content-within', id='index')
            webLink = diseases.find_all('a', href=True)
            
            for link in webLink:

                try:
                    self.verboseprint('[LOG] Retrieving ', link['href'], '...')
                    url = base_url + link['href']

                    time.sleep(5)
                    html_disease = requests.get(url).text
                    
                    
                except:
                    self.verboseprint('[LOG] Retrieval Error')
                    continue
                try:
                    letterSoup = BeautifulSoup(html_disease, 'lxml')
                except:
                    self.verboseprint('[LOG] Soup Error')
                    continue
                    # row = letterSoup.find('div', class_='row')  # disease information
                
                    # headerToLink = row.find('h1')
                try:
                    header = letterSoup.find('h1').find('a', href=link['href']).text  # name of disease
                    self.verboseprint('[LOG] Retrieved ', header, ' data...')
                except:
                    self.verboseprint('[LOG] Header error')
                
                contentInstance = letterSoup.find('div',id='main-content')  # all info on page
                    # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
                
                try:
                    headerLoc = header.find('/')
                    while (headerLoc != -1):
                        headerLoc = header.find('/')
                        header = header.replace('/',' ')
                except:
                    self.verboseprint('[LOG] NoneType object except')
                    continue
                try:
                    with io.open(header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                        f.write(contentInstance.prettify()) 
                except:
                    self.verboseprint('[LOG] Write error')