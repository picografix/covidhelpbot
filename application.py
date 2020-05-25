from flask import Flask, request
import requests
from bs4 import BeautifulSoup as bs
import urllib
from twilio.twiml.messaging_response import MessagingResponse
from random import randint

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.body('Here You Go version 1.01')
        msg.media('https://cataas.com/cat')
        responded = True
    if 'dog' in incoming_msg:
        # return a cat pic
        responseDog=requests.get("https://dog.ceo/api/breeds/image/random")
        l = responseDog.json()
        ans = l['message']
        msg.body('Love <3')
        msg.media(ans)
        responded = True
    if 'wallpaper' in incoming_msg:
        l=incoming_message.split()
        url=l[1]
        try: 
            from googlesearch import search 
        except ImportError:  
            print("No module named 'google' found") 
        
        # to search 
        query = url+" unsplash"
        
        for j in search(query, tld="co.in", num=1, stop=4, pause=2):
            if "https://unsplash.com/s/photos" in j: 
                url=j 
        a=urllib.request.urlopen(url,context=ctx).read()
        soup=bs(a,'html.parser')
        L=soup.find_all('a',{'title':"Download photo"})
        x=randint(1,len(L)-1)
        alink=L[x].get('href')
        msg.media(alink)
        responded=True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry! (ver 1.0.2)')
    return str(resp)


if __name__ == '__main__':
    app.run()
