#webmd
from bs4 import BeautifulSoup
import requests
import time
import io
import os

def webmdDrugs():
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    base_url = 'https://www.webmd.com/'
    # takeRequest = input("Enter base URL to scrape (i.e. https://www.website.org/index/diseases/letter=A\n")
    # html_text = requests.get(takeRequest).text
    time.sleep(5)
    base_html = requests.get("https://www.webmd.com/drugs/2/alpha/a", headers=headers).text

    base_soup = BeautifulSoup(base_html, 'lxml')
    print('Retrieved base indices...')

    if not os.path.exists(originDir + "\\Drugs"):
        os.mkdir(originDir + "\\Drugs")
    os.chdir(originDir + "\\Drugs")

    osDir = originDir + "\\" + "Drugs\\"+ "WebMD"
    if not os.path.exists(osDir):
            os.mkdir(osDir)
    os.chdir(osDir)

    indices = base_soup.find('div', class_='alpha-container')
    indexLinks = indices.find_all('a',href=True)

    for letters in indexLinks:
        letterName = letters.get_text()
        newpath = osDir + "\\" + letterName

        #add redundancy detections
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        os.chdir(newpath)
        url = base_url + letters['href']
        print('Retrieving WebMD URL ',url,'...')

        time.sleep(5)
        htmlText = requests.get(url, headers=headers).text

        soup = BeautifulSoup(htmlText,'lxml')
        print('Retrieved WebMD URL ',url)

        subIndices = soup.find('ul',class_='browse-letters squares sub-alpha')
        subIndexLinks = subIndices.find_all('a',href=True)

        for subLetter in subIndexLinks:
            print('Retrieving WebMD URL ', base_url + subLetter['href'],'...')
            time.sleep(5)
            subHtmlText = requests.get(base_url + subLetter['href'], headers=headers)
            print('Retrieved WebMD URL ', base_url + subLetter['href'])
            subDrugSoup = BeautifulSoup(subHtmlText.text,'lxml')

            subDrug = subDrugSoup.find('div',class_='drugs-search-list-conditions')
            subDrugList = subDrug.find_all('a',href=True)
            
            for drug in subDrugList:
                drugName = drug.get_text()
                drugUrl = base_url + drug['href']

                print('Retrieving WebMD URL ', drugUrl,'...')
                time.sleep(5)
                drugHtml = requests.get(drugUrl, headers=headers)
                print('Retrieved WebMD URL ', drugUrl)
                
                drugSoup = BeautifulSoup(drugHtml.text,'lxml')
                drugInfo = drugSoup.find('div',class_='pane webmd-row')

                #fix file name errors
                errorLoc = drugName.find('/')
                while (errorLoc != -1):
                    drugName = drugName.replace('/',' ')
                    errorLoc = drugName.find('/')
                
                with io.open(drugName+'.txt','w',encoding='utf-8') as f:
                    f.write(drugInfo.prettify())

originDir = os.getcwd() 
webmdDrugs()