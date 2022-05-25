from bs4 import BeautifulSoup
import requests
import time
import io
import os
import multiprocessing


# imports

def mayoclinicDrugs():
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    base_url = 'https://www.mayoclinic.org'
    # takeRequest = input("Enter base URL to scrape (i.e. https://www.website.org/index/diseases/letter=A\n")
    # html_text = requests.get(takeRequest).text
    time.sleep(5)
    base_html = requests.get("https://www.mayoclinic.org/drugs-supplements/drug-list", headers=headers).text
    

    base_soup = BeautifulSoup(base_html, 'lxml')
    print('Retrieved base indices...')
    

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
        print('Getting URL ', get_url, '...')

        time.sleep(5)
        
        html_text = requests.get(get_url, headers=headers).text

        soup = BeautifulSoup(html_text, 'lxml')
        print("Retrieved index...")

        diseases = soup.find('div', class_='index content-within', id='index')
        webLink = diseases.find_all('a', href=True)
        
        
        for link in webLink:

            try:
                print('Retrieving ', link['href'], '...')
                url = base_url + link['href']

                time.sleep(5)
                html_disease = requests.get(url, headers=headers).text
                
                
            except:
                print('Retrieval Error')
                continue
            try:
                letterSoup = BeautifulSoup(html_disease, 'lxml')
            except:
                print('Soup Error')
                continue
                # row = letterSoup.find('div', class_='row')  # disease information
            
                # headerToLink = row.find('h1')
            try:
                header = letterSoup.find('h1').find('a', href=link['href']).text  # name of disease
                print('Retrieved ', header, ' data...')
            except:
                print('Header error')

            
            
            contentInstance = letterSoup.find('div',id='main-content')  # all info on page
                # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
             
            try:
                headerLoc = header.find('/')
                while (headerLoc != -1):
                    headerLoc = header.find('/')
                    header = header.replace('/',' ')
            except:
                print('NoneType object except')
                continue
            try:
                with io.open(header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                    f.write(contentInstance.prettify()) 
            except:
                print('Write error')

def mayoclinicDiseasesAndConditions():
    base_url = 'https://www.mayoclinic.org'
    # takeRequest = input("Enter base URL to scrape (i.e. https://www.website.org/index/diseases/letter=A\n")
    # html_text = requests.get(takeRequest).text
    base_html = requests.get("https://www.mayoclinic.org/diseases-conditions").text
    base_soup = BeautifulSoup(base_html, 'lxml')
    print('Retrieved base indices...')
    time.sleep(5)

    osDir = originDir + "\\" + "Conditions\\"+"mayoclinicConditions"
    if not os.path.exists(osDir):
            os.mkdir(osDir)

    indices = base_soup.find('ol', class_='acces-alpha')
    indexLinks = indices.find_all('a', href=True)
    
    for indexLetters in indexLinks: #add this stuff into a queue
        letterName = indexLetters.select('span')[1].get_text()
        newpath = osDir + "\\" + letterName
        
        nextLetter = chr(ord(letterName)+1)
        testPath = osDir + "\\" + nextLetter

        if os.path.exists(testPath):
            continue

        if not os.path.exists(newpath):
            os.mkdir(newpath)

        os.chdir(newpath)

        get_url = base_url + indexLetters['href']
        print('Getting URL ', get_url, '...')

        html_text = requests.get(get_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        print("Retrieved index...")

        diseases = soup.find('div', class_='index content-within', id='index')
        webLink = diseases.find_all('a', href=True)

        time.sleep(5)
        for link in webLink:
            print('Retrieving ', link['href'], '...')
            url = base_url + link['href']
            html_disease = requests.get(url).text

            letterSoup = BeautifulSoup(html_disease, 'lxml')
            row = letterSoup.find('div', class_='row')  # disease information

            try:
                header = row.find('a', href=link['href']).text  # name of disease
                print('Retrieved ', header, ' data...')

                contentInstance = letterSoup.find('div', class_='content')  # all info on page
                # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
                
                try:
                    headerLoc = header.find('/')
                    while (headerLoc != -1):
                        headerLoc = header.find('/')
                        header = header.replace('/',' ')
                except:
                    print('NoneType object except')
            except:
                print('NoneType Header Error')

        

            try:
                with io.open(header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                    f.write(contentInstance.get_text()) #change to without text to preserve formatting. fuck
            except:
                print("Error occurred in write")
            # according to google, ethical text scraping waits 5 seconds
            time.sleep(5)

originDir = os.getcwd() 
mayoclinicDrugs()
# mayoclinicDiseasesAndConditions()