from bs4 import BeautifulSoup
import requests
import time
import io
import os

def template():
    originDir = os.getcwd() #get your directory (currently only supports windows, only three changes need to be made to fix)
    headers = {'user-agent':'<your user agent>'} #add any functioning user agents    base_url = 'https://www.<website>'
    base_url = 'https://www.<website>.<ext (gov,com, etc)>'
    time.sleep(5)
    base_html = requests.get("<url of drug/disease index>",headers=headers).text 

    base_soup = BeautifulSoup(base_html, 'lxml')
    print('Retrieved base indices...')

    if not os.path.exists(originDir + "\\<output type, i.e. drugs>"): #Drugs or Diseases or other category for file path
        os.mkdir(originDir + "<output type, i.e. drugs>")
    os.chdir(originDir + "\\<output type, i.e. drugs>")

    osDir = originDir + "\\" + "<output type, i.e. drugs>\\"+ "<website name>"
    if not os.path.exists(osDir):
            os.mkdir(osDir)
    os.chdir(osDir)

    indices = base_soup.find('<html identifier i.e. div, ul, li, etc of href container>', class_='<class of identifier>')
    indexLinks = indices.find_all('a',href=True)

    for letters in indexLinks:
        letterName = letters.get_text()
        newpath = osDir + "\\" + letterName

        if not os.path.exists(newpath):#check for redundancies
            os.mkdir(newpath)
        os.chdir(newpath)
        url = base_url + letters['href']
        print('Retrieving <website> URL ',url,'...')

        time.sleep(5)
        htmlText = requests.get(url).text

        soup = BeautifulSoup(htmlText,'lxml')
        print('Retrieved <website> URL ',url)

        subIndices = soup.find('<html identifier i.e. div, ul, li, etc of href container>', class_='<class of identifier>')
        subIndexLinks = subIndices.find_all('a',href=True)

        for subLetter in subIndexLinks:
            print('Retrieving <website> URL ', base_url + subLetter['href'],'...')
            time.sleep(5)
            subHtmlText = requests.get(base_url + subLetter['href'],headers=headers)
            print('Retrieved <website> URL ', base_url + subLetter['href'])
            suboutSoup = BeautifulSoup(subHtmlText.text,'lxml')

            subOutput = suboutSoup.find('<html identifier i.e. div, ul, li, etc of href container>', class_='<class of identifier>')
            subOutputList = subOutput.find_all('a',href=True)
            
            for output in subOutputList:
                outputName = output.get_text()
                outputUrl = base_url + output['href']

                print('Retrieving <website> URL ', outputUrl,'...')
                time.sleep(5)
                outHtml = requests.get(outputUrl)
                print('Retrieved <website> URL ', outputUrl)
                
                outSoup = BeautifulSoup(outHtml.text,'lxml')
                info = outSoup.find('<html identifier i.e. div, ul, li, etc of href container>', class_='<class of identifier>')#find name of output/disease

                #fix file name errors
                errorLoc = outputName.find('/')
                while (errorLoc != -1):
                    outputName = outputName.replace('/',' ')
                    errorLoc = outputName.find('/')
                
                with io.open(outputName+'.txt','w',encoding='utf-8') as f: #write to file
                    f.write(info.prettify())


template()
