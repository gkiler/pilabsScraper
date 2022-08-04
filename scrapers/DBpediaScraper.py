from scrapers.WebsiteScraper import WebsiteScraper

import time 
import requests # for requsting urls
import os # provides functions for creating and removing a directory (folder)
from bs4 import BeautifulSoup
import io # allows us to manage file-related input and output operations
import json # for json outputting
from os.path import exists
from datetime import datetime
from pathvalidate import sanitize_filename #not native


class DBpediaScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd() #Get current dir for file pathing
        headers = self._headers #Many websites prevent scraping from default clients, so provide a client header such as firefox information
        base_url = self._base_url 
        time.sleep(5) #Scrapers must wait 5 seconds between requests else risking getting IP banned
        base_html = requests.get(self._base_url + "page/Category:Lists_of_diseases", headers=headers).text # Retrieve base index page to retrieve other index link

        base_soup = BeautifulSoup(base_html, 'lxml') #Create BS object to parse html
        print('[DBpedia]Retrieved base indices...')

        diseaseAndConditions = originDir + "\\DiseasesAndConditions"
        if not os.path.exists(diseaseAndConditions): # if path dne create diseases and conditions directory in originDir
            os.mkdir(diseaseAndConditions) # makes new folder

        osDir = diseaseAndConditions + "\\" + "DBpedia" # if dne, create FamilyDoctor directory
        if not os.path.exists(osDir):
            os.makedirs(osDir) # creates new folder as well as sub-folder (for all letters)

        container = base_soup.find_all('ul')[12]
        #print(container)
        websitelinks = container.find_all('a', href=True)
        # #print(websitelinks)

        linkCounter = 0  #to check if the folder for the next link exists
        for link in websitelinks:
            #make new directory    
            linkName = "".join(x for x in link.get_text() if x.isalnum()) #verify folder name can be made, remove spaces or any weird occurences
            linkfolder = osDir + "\\" + linkName.strip() 

            nextlink = container.find_all('a', href=True)[linkCounter]
            print(nextlink) 
            nextLinkName = "".join(x for x in nextlink.get_text() if x.isalnum()) #verify folder name can be made, remove spaces or any weird occurences
            nextLinkfolder = osDir + "\\" + nextLinkName.strip()  
            # print(nextLinkfolder)
            if os.path.exists(nextLinkfolder):
                # linkCounter+=1
                continue #skip this iteration of for loop         
            elif os.path.exists(linkfolder):
                os.makedirs(linkfolder)

            linkCounter +=1
            print(linkCounter)

            url = link['href'] #Form complete url from href
            print(url)
            print('Retrieving container URL ',url,'...')

            time.sleep(5) # wait 5 seconds, then request
            htmlText = requests.get(url, headers=headers).text

            soup = BeautifulSoup(htmlText, 'lxml')
            print('[DBpedia]Retrieved DBpedia URL ',url) 

            subcontainer = soup.find_all('ul')[9] #This website contains subletters such as Aa Ab Ac and so on under A, with Ba Bb under B and so on.
            #print(subcontainer)                                                                       #These are contained within the class stated in the statement
            subIndexLinks = subcontainer.find_all('a',href=True) #Retrieve indices

            for disease in subIndexLinks: 
                diseaseName = disease.get_text() #retrieve name of disease from html element
                diseaseUrl = base_url + "/" + disease['href'] #form disease link

                #print('[DBpedia]Retrieving DBpedia URL ', diseaseUrl,'...')
                time.sleep(5)
                diseaseHtml = requests.get(diseaseUrl, headers=headers) #wait and request
                print('[DBpedia]Retrieved DBpedia URL ', diseaseUrl)
                
                diseaseSoup = BeautifulSoup(diseaseHtml.text,'lxml') #soup

                fileName = sanitize_filename(diseaseName) #ensure diseases with names including backslashes or other non alphanumeric chars lose that information to not break file naming.
                jsonPath = linkfolder + "/" + fileName + ".json"  #create json path                 
                
                                    
                date = datetime.now() #date scraped
                
                data = { #json formatting of data in a python list object containing disease name, untouched html, origin url, date scraped, and source name
                        "name": diseaseName,
                        "raw_html": diseaseSoup.prettify(),
                        "source_url": url,
                        "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                        "source_name": "DBpedia"
                    }
                
                with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                    json.dump(data, file, indent = 4) #store "data" as json file

            # linkCounter +=1
            # print(linkCounter)
            