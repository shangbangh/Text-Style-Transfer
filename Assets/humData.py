'''
Created on July 13, 2020

@author: myuey
'''
import requests
from bs4 import BeautifulSoup
import re
import codecs
from textblob import TextBlob
import time
import random

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}

#text collector for isolated chapters on tumblr
def indChapGetTumblr(title, chapInd):
    targetUrl =  "https://blastron01.tumblr.com/post/181369364884/ascendance-of-a-bookworm-096"
    targetPage = requests.get(targetUrl, headers = header)
    targetSoup = BeautifulSoup(targetPage.content, 'html.parser')
    for item in targetSoup.find_all("ul", class_="meta"):
        item.decompose()
    for item in targetSoup.find_all("div", class_="permalink-footer clearfix"):
        item.decompose()    
    text = targetSoup.find("div", class_= "post text").text
    tblo = TextBlob(text)    
    #create list of sentences
    res = []
    for sentence in tblo.sentences:
        res.append("".join(sentence))
    #remove the title from the first sentence
    res[0] = res[0].replace(title,title + "\n\n")
    #remove the ending from the last sentence
    res[-1] = res[-1].replace("prev • next", '')
    folderStr = "./humTransDataAscB/"
    chapFile = folderStr + "Ch. " + str(chapInd) + ".txt"
    with codecs.open(chapFile, mode="w", encoding="utf-8") as f:
        for sentence in res:          
            f.write(sentence + "\n")
  
#gets an individual chapter  
def indChapGet():
    pass
    
#opens and extracts the links from the table of contents for ascendance book translator 1
def access_toc_ASCBOOK1():
    targetUrl =  "https://blastron01.tumblr.com/honzuki-contents"
    targetPage = requests.get(targetUrl, headers = header)
    targetSoup = BeautifulSoup(targetPage.content, 'html.parser')
    
    #exclude_classes = []
    #for div in targetSoup.find_all("div", {'class':exclude_classes}): 
        #div.decompose()
    for item in targetSoup.find_all("header"):
        item.decompose()    
    links = []
    for link in targetSoup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link)
    links.pop(-1)   
    links.pop(0)
    return links
#loops through list of links, accessing each and pulling text
def get_data_ASCBOOK1():
    linkList = access_toc_ASCBOOK1()
    folderStr = "./humTransDataAscB/"
    startInd = 1
    for link in linkList:
        #pull chapter webpage
        targetUrl = link.get("href")
        targetPage = requests.get(targetUrl, headers = header)
        targetSoup = BeautifulSoup(targetPage.content, 'html.parser')
        title = ''.join([i for i in link.text if not i.isdigit()])
        for item in targetSoup.find_all("ul", class_="meta"):
            item.decompose()
        for item in targetSoup.find_all("div", class_="permalink-footer clearfix"):
            item.decompose()  
        text = targetSoup.find("div", class_= "post text").text
        tblo = TextBlob(text)    
        #create list of sentences
        res = []
        for sentence in tblo.sentences:
            res.append("".join(sentence))
        #remove the title from the first sentence
        res[0] = res[0].replace(title,title + "\n\n")
        #remove the ending from the last sentence
        res[-1] = res[-1].replace("prev • next", '')
        chapFile = folderStr + "Ch. " + str(startInd) + ".txt"
        with codecs.open(chapFile, mode="w", encoding="utf-8") as f:
            for sentence in res:          
                f.write(sentence + "\n")
        startInd += 1
def get_data_ASCBOOK2():
    targetUrl = "https://infinitenoveltranslations.net/teasers/ascendance-of-a-bookworm/chapter-91-100/chapter-103-a-family-council-in-the-temple/"
    folderStr = "./humTransDataAscB/"
    chapInd = 103
    targetPage = requests.get(targetUrl, headers = header)
    targetSoup = BeautifulSoup(targetPage.content, 'html.parser')    
    title = targetSoup.find("h1", class_="entry-title").text
    textSoup = targetSoup.find("div", class_="entry-content")
    chapFile = folderStr + "Ch. " + str(chapInd) + ".txt"
    with codecs.open(chapFile, mode="w", encoding="utf-8") as f:
        f.write(title)
        f.write(textSoup.text)

def get_slime_chap(title,target, isClown):
    if(isClown):
        return ""
    else:
        targetPage = requests.get(target, headers = header)
        targetSoup = BeautifulSoup(targetPage.content, 'html.parser')    
        targetSection = targetSoup.find("div", class_="post-body entry-content")
        for item in targetSection.find_all("div", class_=["MsoEndnoteText", "post-footer"]):
            item.decompose()
        targetText = targetSection.text
        #Remove translator notes at beginning
        titleInd = targetText.find(title)
        targetText = targetText[titleInd:]
        return targetText
        
        
    
def get_data_slime():
    targetUrl = "http://gurotranslation.blogspot.com/p/ioduction.html"
    targetPage = requests.get(targetUrl, headers = header)
    targetSoup = BeautifulSoup(targetPage.content, 'html.parser')    
    folderStr = "./humTransDataSlime/"
    links = []
    for item in targetSoup.find_all("img"):
        item.decompose()
    for item in targetSoup.find_all("a", class_=["home-link", "feed-link", "quickedit"]):
        item.decompose()
    for item in targetSoup.find_all("div", id = ["navbar","comments"]):
        item.decompose()    
    for item in targetSoup.find_all("div", class_=["widget-content", "post-footer", "sidebar-section"]):
        item.decompose()
    for link in targetSoup.findAll('a'):
        links.append(link)
    del links[0:9]
    links.pop(29)
    links.pop(47)
    links.pop(47)
    links.pop(67)
    links.pop(67)
    links.pop(87)
    links.pop(158)
    links.pop(251)
    #manually do chapter 137: p1 and p2
    links.pop(140)
    links.pop(141)
    chapInd = 1
    for link in links:  
        #determine if the link is to guro or to clown
        title = link.text
        chapText = get_slime_chap(title, link, "clown" in link.get('href'))
        chapFile = folderStr + "Ch. " + str(chapInd) + ".txt"
        
        with codecs.open(chapFile, mode="w", encoding="utf-8") as f:
            f.write(title)
            f.write(chapText)
        #add randomness to access times as site displays visitors
        time.sleep(620 + random.randint(420,501))
def get_data_DBDa():
    #get toc page
    targetUrl = "https://starrynightnovels.com/dukes-daughter-and-the-seven-nobles/"
    targetPage = requests.get(targetUrl, headers = header)
    targetSoup = BeautifulSoup(targetPage.content, 'html.parser') 
    folderStr = "./humTransDataDBDa/"
    links = []
    linkSoup = targetSoup.find("div", class_="entry-content")
    for link in linkSoup.find_all("a"):
        links.append(link)
    #clean link list
    del links[0:15]  
    del links[len(links)-4:] 
    links.pop(19)
    #use link text for chapter title text
    linkInd = 1
    for link in links:
        contents = get_chap_DBDa(link.get('href'))
        title = link.text
        chapFile = folderStr + "Ch. " + str(linkInd) + ".txt"
        with codecs.open(chapFile, mode="w", encoding="utf-8") as f:
            f.write(title)
            f.write("\n")
            f.write(contents)
        linkInd += 1

def get_chap_DBDa(link):
    targetPage = requests.get(link, headers = header)
    targetSoup = BeautifulSoup(targetPage.content, 'html.parser') 
    targetSection = targetSoup.find("div", class_="entry-content")
    #locate second instance of superscript 1 in the tagged section
    targetHtmlStr = str(targetSection)
    ind1 = targetHtmlStr.find("<sup>1")

    #remove end links flag
    endLinksFlag = False
    if(ind1 > 0):
        #footnotes found
        str_mod = targetHtmlStr[ind1 + 6:]
        ind2 = str_mod.find("<sup>1")
        targetHtmlStr = targetHtmlStr[:ind1+ind2+6]
    else:
        endLinksFlag = True
    #remove all tags after it
    #delete all 
    convSoup = BeautifulSoup(targetHtmlStr, 'html.parser')
    for item in convSoup.find_all(["sup","figure"]):
        item.decompose()
    targetText = convSoup.text
    #locate first instance of >>
    indexHead = targetText.find("r >>")
    targetText = targetText[indexHead + 4:]
    if(endLinksFlag):
        indexEnd = targetText.find("<< P")
        targetText = targetText[:indexEnd]
    ind_check_edit = targetText.find("Edit")
    if(ind_check_edit > 0):
        print(link)
        print(ind_check_edit)
    
    return targetText

get_data_DBDa()

    
