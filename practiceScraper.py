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

class FamilyDoctorScraper(WebsiteScraper):
    def scrape(self):
        originDir = os.getcwd() #Get current dir for file pathing
        headers = self._headers #Many websites prevent scraping from default clients, so provide a client header such as firefox information
        base_url = self._base_url #Base url being https://www.WebMD.com
        time.sleep(5) #Scrapers must wait 5 seconds between requests else risking getting IP banned
        base_html = requests.get(self._base_url + "/diseases-and-conditions/?alpha=A", headers=headers).text # Retrieve base index page to retrieve other index link

        base_soup = BeautifulSoup(base_html, 'lxml') #Create BS object to parse html
        print('[FAMILYDOCTOR] Retrieved base indices...')

        diseasePath = originDir + "\\Disease" #variable not being used
        if not os.path.exists(diseasePath): #if not exists, create drugs directory in originDir
            os.mkdir(diseasePath)

        osDir = diseasePath + "\\"  + "FamilyDoctor" #if not exists, create WebMD directory
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        indices = base_soup.find('div', class_='facet-container facet-alpha clearfix') #index hyperlinks to each letter of the alphabet contained here

        indexLinks = indices.find_all('a',href=True) #retrieve all href links within the container

        for letters in indexLinks: #iterate through each hyperlink
            letterName = "".join(x for x in letters.get_text() if x.isalnum()) #verify folder name can be made, remove spaces or any weird occurences
            newpath = osDir + "\\" + letterName.strip() #retrieve the letter name from the html element
            print (letterName)
            nextLetter = chr(ord(letterName)+1) #Assume that if the next letter exists, this current letter has been completely scraped.
#                                                 #TODO: Small error where indexes labelled "#" or "0-9" cannot be scraped as they are not alphanumeric. Add try catch statement
            testPath = osDir + "\\" + nextLetter 
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)
            url = letters['href'] # Form complete url from href
            print('[FAMILYDOCTOR] Retrieving WebMD URL ',url,'...') 

            time.sleep(5) # Wait 5 seconds, then request
            htmlText = requests.get(url, headers=headers).text

            soup = BeautifulSoup(htmlText,'lxml') #Soup
            print('[FAMILYDOCTOR] Retrieved WebMD URL ',url) 
            
            #next_page_url = soup.find('li',class_='next') #can use li since I'm only checking for a single "next" link and I don't need to grab all the subletter links
            
            while True:
                time.sleep(5)#wait 5 seconds, then request

                htmlText = requests.get(url, headers=headers).text
                soup = BeautifulSoup(htmlText,'lxml')

                drugs = soup.find('div', id="search-results")
                webLink = drugs.find_all('a', href=True, attrs={"class" : "link-to-post"})

                for link in webLink:
                    diseaseName = link.get_text() #retrieve name of drug from html element
                    drugUrl = link['href'] #form drug link

                    print('[FAMILYDOCTOR] Retrieving WebMD URL ', drugUrl,'...')
                    time.sleep(5)
                    drugHtml = requests.get(drugUrl, headers=headers) #wait and request
                    print('[FAMILYDOCTOR] Retrieved WebMD URL ', drugUrl)
                    
                    drugSoup = BeautifulSoup(drugHtml.text,'lxml') #soup

                    fileName = sanitize_filename(diseaseName) #ensure drugs with names including backslashes or other non alphanumeric chars lose that information to not break file naming.
                    jsonPath = newpath + "/" + fileName + ".json"  #create json path                 
                    
                    date = datetime.now() #date scraped
                    
                    data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                            "name": diseaseName,
                            "raw_html": drugSoup.prettify(),
                            "source_url": url,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "WebMD"
                        }

                # how to go to next page
                next_page_url = soup.find('li', attrs={"class": "next"})
                # print(next_page_url)
                if next_page_url:
                    next_page_url = next_page_url.find("a", href=True)
                    url = next_page_url['href']
                    print(url)
                else:
                    break

          