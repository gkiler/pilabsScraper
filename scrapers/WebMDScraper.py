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
        originDir = os.getcwd() #Get current dir for file pathing
        headers = self._headers #Many websites prevent scraping from default clients, so provide a client header such as firefox information
        base_url = self._base_url #Base url being https://www.WebMD.com
        time.sleep(5) #Scrapers must wait 5 seconds between requests else risking getting IP banned
        base_html = requests.get(self._base_url + "/drugs/2/alpha/a", headers=headers).text # Retrieve base index page to retrieve other index link

        base_soup = BeautifulSoup(base_html, 'lxml') #Create BS object to parse html
        print('[WEBMD]Retrieved base indices...')

        if not os.path.exists(originDir + "\\Drugs"): #if not exists, create drugs directory in originDir
            os.mkdir(originDir + "\\Drugs")
        drugsPath = originDir + "\\Drugs"

        osDir = originDir + "\\" + "Drugs\\" + "WebMD" #if not exists, create WebMD directory
        if not os.path.exists(osDir):
                os.makedirs(osDir)

        indices = base_soup.find('div', class_='alpha-container') #index hyperlinks to each letter of the alphabet contained here
        indexLinks = indices.find_all('a',href=True) #retrieve all href links within the container

        for letters in indexLinks: #iterate through each hyperlink
            letterName = "".join(x for x in letters.get_text() if x.isalnum()) #verify folder name can be made, remove spaces or any weird occurences
            newpath = osDir + "\\" + letterName.strip() #retrieve the letter name from the html element

            nextLetter = chr(ord(letterName)+1) #Assume that if the next letter exists, this current letter has been completely scraped.
                                                #TODO: Small error where indexes labelled "#" or "0-9" cannot be scraped as they are not alphanumeric. Add try catch statement
            testPath = osDir + "\\" + nextLetter 
            if os.path.exists(testPath):
                continue
            elif (not os.path.exists(newpath)):
                os.makedirs(newpath)
                                               
            url = base_url + "/" + letters['href'] #Form complete url from href
            print('[WEBMD]Retrieving WebMD URL ',url,'...') 

            time.sleep(5)#wait 5 seconds, then request
            htmlText = requests.get(url, headers=headers).text

            soup = BeautifulSoup(htmlText,'lxml') #Soup
            print('[WEBMD]Retrieved WebMD URL ',url) 

            subIndices = soup.find('ul',class_='browse-letters squares sub-alpha') #This website contains subletters such as Aa Ab Ac and so on under A, with Ba Bb under B and so on.
                                                                                   #These are contained within the class stated in the statement
            subIndexLinks = subIndices.find_all('a',href=True) #Retrieve indices

            for subLetter in subIndexLinks: #Iterate through subletters
                print('[WEBMD]Retrieving WebMD URL ', base_url + "/" + subLetter['href'],'...')
                time.sleep(5)
                subHtmlText = requests.get(base_url + subLetter['href'], headers=headers) #wait and request
                print('[WEBMD]Retrieved WebMD URL ', base_url + subLetter['href'])
                subDrugSoup = BeautifulSoup(subHtmlText.text,'lxml') #soup

                try:
                    subDrug = subDrugSoup.find('div',class_='drugs-search-list-conditions') #Drug hyperlinks are contained within this class
                                                                                                
                                                                                            #numerous try catch statements ensure that the entire program doesn't break if one website breaks.
                                                                                            #this can be improved on by adding error logging for when specific crashes occur and saving the log. Other websites are missing this feature
                    subDrugList = subDrug.find_all('a',href=True) #retrieve all drug
                except:
                    continue
                for drug in subDrugList:
                    drugName = drug.get_text() #retrieve name of drug from html element
                    drugUrl = base_url + "/" + drug['href'] #form drug link

                    print('[WEBMD]Retrieving WebMD URL ', drugUrl,'...')
                    time.sleep(5)
                    drugHtml = requests.get(drugUrl, headers=headers) #wait and request
                    print('[WEBMD]Retrieved WebMD URL ', drugUrl)
                    
                    drugSoup = BeautifulSoup(drugHtml.text,'lxml') #soup

                    fileName = sanitize_filename(drugName) #ensure drugs with names including backslashes or other non alphanumeric chars lose that information to not break file naming.
                    jsonPath = newpath + "/" + fileName + ".json"  #create json path                 
                    
                                        
                    date = datetime.now() #date scraped
                    
                    data = { #json formatting of data in a python list object containing drug name, untouched html, origin url, date scraped, and source name
                            "name": drugName,
                            "raw_html": drugSoup.prettify(),
                            "source_url": url,
                            "date_time_scraped": date.strftime("%d/%m/%Y %H:%M:%S"),
                            "source_name": "WebMD"
                        }
                    
                    with io.open(jsonPath, 'w+', encoding='utf-8') as file:
                        json.dump(data, file, indent = 4) #store "data" as json file
