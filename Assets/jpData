'''
Created on May 26, 2020

@author: myuey
'''
import requests
from bs4 import BeautifulSoup
import codecs

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def printLinkList(listPrint):
    i = 0
    for entry in listPrint:
        print(i,entry.text)
        i+=1

def testDataCollect():
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    targetUrl =  "https://www.sousetsuka.com/2015/04/death-march-kara-hajimaru-isekai_23.html"
    targetPage = requests.get(targetUrl, headers = header)
    targetSoup = BeautifulSoup(targetPage.content, 'html.parser')
    folderStr = "./jpRawDataDeaM/"
   
def renumber(chapInd, excludeList):
    if len(excludeList) == 0:
        return chapInd
    if(chapInd < excludeList[0]):
        return chapInd
    #loop through exclude list and compare numbers to chapter index
    i = 1
    while i < len(excludeList):
        num = excludeList[i]
        if(chapInd < num):
            return chapInd - i
        i+=1
  
    return chapInd - i

def GetJPData():
    #chapter url format
    #dragon egg
    #urlBase = "https://ncode.syosetu.com/n4698cv/"
    #Spider desu ka
    #urlBase = "https://ncode.syosetu.com/n7975cr/"
    #DeaM
    #urlBase = "https://ncode.syosetu.com/n9902bn/"
    #AscB
    #urlBase = "https://ncode.syosetu.com/n4830bu/"
    #DBDa
    urlBase = "https://ncode.syosetu.com/n8204cp/"
    #create target numbers for chapters to pull
    chapStart = 1
    chapEnd = 164
    #DeaM list
    #excludeList = [11, 24, 25, 34, 48, 49, 67, 113, 114, 115, 142, 144, 183, 184, 227, 300, 301, 336, 374]
    #Slime list
    excludeList = []
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    folderStr = "./jpRawDataDBDa/"
    
    chapInd = chapStart
    
    while chapInd < chapEnd + 1:
        if(chapInd in excludeList):
            pass
        else:
            chapUrl = urlBase + str(renumber(chapInd, excludeList)) + '/'
            
            chapPage = requests.get(chapUrl, headers = header)
            chapSoup = BeautifulSoup(chapPage.content, 'html.parser')
            #pull title
            title = chapSoup.find("p", class_="novel_subtitle").text
            #pull text
            text = chapSoup.find("div", id = "novel_honbun").text
            #write file
            
            chapInd = renumber(chapInd, excludeList)
            chapFile = folderStr + "Ch. " + str(chapInd) + ".txt"
            with codecs.open(chapFile, mode="w", encoding="utf-8") as f:
                f.write(title + '\n')
                f.write(text)
        chapInd += 1
GetJPData()  
        
        
