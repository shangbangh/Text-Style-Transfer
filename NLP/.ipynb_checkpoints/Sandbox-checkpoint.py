# from textblob import TextBlob
from NLP import DataProcess as DP
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentPoolEmbeddings, Sentence
# import requests
# from bs4 import BeautifulSoup
# import regex as re

tr = open("../Assets/eng/110.txt")
sentence = Sentence(tr.read(), use_tokenizer=True)
# eng_excluded_classes = ['comment-content', 'comment-respond', 'sidebar-inner-widget']
# eng_url = "https://dsrealmtranslations.com/table-of-contents/ch-110-king-centipede/"
# headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
# eng = DP.scrap_text(eng_url,headers,eng_excluded_classes)
# trBlob = TextBlob(tr)

mt = open("../Assets/mt/110.txt")
# mtBlob = TextBlob(mt)


# jp = open("../Assets/jp/110.txt", encoding='utf-8')
# jp_excluded_classes = ['contents1','novel_attention']
# jp_url = "http://ncode.syosetu.com/n4698cv/110/"
# jp = DP.scrap_text(jp_url, headers, jp_excluded_classes)
# 
# regex = "[0-9]+\.[\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+\n"
# title = re.search(regex, jp)
# jp = jp[title.end():]
# jpBlob = TextBlob(jp.read())


# initialize the word embeddings
glove_embedding = WordEmbeddings('glove')
flair_embedding_forward = FlairEmbeddings('news-forward')
flair_embedding_backward = FlairEmbeddings('news-backward')

# initialize the document embeddings, mode = mean
document_embeddings = DocumentPoolEmbeddings([glove_embedding,
                                              flair_embedding_backward,
                                              flair_embedding_forward])
document_embeddings.embed(sentence)
print(sentence.get_embedding())