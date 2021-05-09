# pylint: disable=C0103, C0111, R0914

'''
Make the request to the inshorts url according to category with requests module.
Parse using beautiful soup and lxml to form the newsDictionary.
'''

import requests
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 

def getNews(category):
    newsDictionary = {
        'success': True,
        'category': category,
        'data': []
    }
    query = category+" inshorts"
    for j in search(query, tld="co.in", num=1, stop=2, pause=2):
        url=j 
        try:
            htmlBody = requests.get(url)
        except requests.exceptions.RequestException as e:
            newsDictionary['success'] = False
            newsDictionary['errorMessage'] = str(e.message)
            return newsDictionary

        soup = BeautifulSoup(htmlBody.text, 'lxml')
        newsCards = soup.find_all(class_='news-card')
        if not newsCards:
            newsDictionary['success'] = False
            newsDictionary['errorMessage'] = 'Invalid Category'
            return newsDictionary

        for card in newsCards:
            try:
                title = card.find(class_='news-card-title').find('a').text
            except AttributeError:
                title = None

            try:
                imageUrl = card.find(
                    class_='news-card-image')['style'].split("'")[1]
            except AttributeError:
                imageUrl = None

            try:
                url = ('https://www.inshorts.com' + card.find(class_='news-card-title')
                      .find('a').get('href'))
            except AttributeError:
                url = None

            try:
                content = card.find(class_='news-card-content').find('div').text
            except AttributeError:
                content = None

            try:
                author = card.find(class_='author').text
            except AttributeError:
                author = None

            try:
                date = card.find(clas='date').text
            except AttributeError:
                date = None

            try:
                time = card.find(class_='time').text
            except AttributeError:
                time = None

            try:
                readMoreUrl = card.find(class_='read-more').find('a').get('href')
            except AttributeError:
                readMoreUrl = None

            newsObject = {
                'title': title,
                'imageUrl': imageUrl,
                'url': url,
                'content': content,
                'author': author,
                'date': date,
                'time': time,
                'readMoreUrl': readMoreUrl
            }

            newsDictionary['data'].append(newsObject)

    return newsDictionary

# print(len(getNews("disease")['data']))
