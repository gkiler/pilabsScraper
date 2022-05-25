#ul class alpha-links

#then ul id="index"

#then div id="mplus-content"


import time
import requests
import os
from bs4 import BeautifulSoup
import io

def medlineDrugs():
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

    originDir = os.getcwd()

    base_url = 'https://medlineplus.gov/' #https://medlineplus.gov/druginfo/drug_Aa.html
    # fin_url = base_url + "/".join(self._ext)
    base_url2 = base_url + 'druginfo/'
    time.sleep(5)
    base_html = requests.get('https://medlineplus.gov/druginformation.html', headers=headers)

    base_soup = BeautifulSoup(base_html.text, 'lxml')
    print(f'[LOG] Retrieved base indices...')

    osDir = originDir + "\\" + "Drugs\\" "medlineDrugs"
    if not os.path.exists(osDir):
        os.mkdir(osDir)

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
            os.mkdir(newpath)

        os.chdir(newpath)

        get_url = base_url + indexLetters['href']
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
                url = base_url2 + tempLink
                print('[LOG] Retrieving ', url, '...')

                time.sleep(5)
                html_drugs = requests.get(url, headers=headers).text
                
                
            except:
                print('[LOG] Retrieval Error')
                continue
            try:
                letterSoup = BeautifulSoup(html_drugs, 'lxml')
            except:
                print('[LOG] Soup Error')
                continue
                # row = letterSoup.find('div', class_='row')  # disease information
            
                # headerToLink = row.find('h1')
            try:
                header = letterSoup.find('h1').text # name of disease
                print('[LOG] Retrieved ', header, ' data...')
            except:
                print('[LOG] Header error')
            
            contentInstance = letterSoup.find('div',id='mplus-content')  # all info on page
                # subContentInstance = contentInstance.select('div')[2].get_text() #sub info of disease #commented due to bug with non uniform webpages
            
            try:
                headerLoc = header.find('/')
                while (headerLoc != -1):
                    headerLoc = header.find('/')
                    header = header.replace('/',' ')
            except:
                print('[LOG] NoneType object except')
                continue
            try:
                with io.open(header + '.txt', 'w', encoding='utf-8') as f:  # write to file
                    f.write(contentInstance.prettify()) 
            except:
                print('[LOG] Write error')
medlineDrugs()