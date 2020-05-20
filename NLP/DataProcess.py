# from keras.preprocessing.text import Tokenizer
import requests
from bs4 import BeautifulSoup
'''
Created on May 19, 2020

@author: Shangbang
'''

def scrap_text(url,headers,exclude_classes=[]):
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content)
    for div in soup.find_all("div", {'class':exclude_classes}): 
        div.decompose()
    mydivs = soup.findAll("p")
    text = ""
    for div in mydivs:
        text += div.text + "\n\n"
    return text

# def create_tokenizer(text):
#     tokenizer = Tokenizer()
#     tokenizer.fit_on_texts(text)
#     return tokenizer