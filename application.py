from flask import Flask, request
import requests
from bs4 import BeautifulSoup as bs
import urllib
from twilio.twiml.messaging_response import MessagingResponse
from random import randint
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import twitter
import datetime
from config import creds

from news import getNews

import cowin
import statistics



app = Flask(__name__)
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    incoming_num1 = request.values.get('To', '').lower() #although not necessary but still
    incoming_num2  = request.values.get('From', '').lower()#the incoming message mobile number
    current = str(datetime.datetime.now())  
    resp = MessagingResponse()
    msg = resp.message()
    completionMsg = "" #this is to store the displayed result
    responded = False
    now = datetime.datetime.now()
    # now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    
    logs="Current Time =", current_time+ incoming_num2 + "Message : "+ incoming_msg
    print(logs)
    if 'bothelp' in incoming_msg:
        
        reply = "Hi I am PicoBot, How can I help you ?\n\nType 'contact' for developers contact \n\nType 'tasks' for list of available tasks"
        msg.body(reply)
        # msg.body("test msg")
        responded=True
        completionMsg=reply
    elif ('covidhelp' in incoming_msg):
        l= incoming_msg.split()
        reply = ""
        try:
            city = l[1]
            required = l[2]
            leads = twitter.input_triggers_spinner(city,required)
            print("Lead length=")
            print(len(leads))
            
            for lead in leads:
                reply += "\n"+lead['full_text']+ "\n-----------------"
        except:
            reply= "Please put your query in given format"
        msg.body(reply)
        responded=True
        completionMsg=reply

    elif('covidnews' in incoming_msg):
        l= incoming_msg.split()
        reply = ""
        try:
            category = l[1]
            news = getNews(category)
            newstock=news["data"]
            for i in range(len(newstock)):
                reply+=news["data"][i]["title"]+"\n\n"+news["data"][i]["content"]
                alink=news["data"][i]["imageUrl"]
            msg.media(alink)
        except:
            reply= "Please put your query in given format"
        msg.body(reply)
        responded=True
        completionMsg=reply

    elif('covidvaccine' in incoming_msg):
        if('drive' in incoming_msg):
            
            reply = cowin.states()
            msg.body(reply)
            responded=True
            completionMsg=reply
        elif('state' in incoming_msg):
            
            l=incoming_msg.split()
            id= int(l[2])
            reply= cowin.districts(id)
            # except:
            #     reply= "Please put your query in given format"     
            msg.body(reply)
            responded=True
            completionMsg=reply
        else:
            l= incoming_msg.split()
            reply = ""
            # try:
                
            #     pincode = l[1]
            #     date = l[2]
            #     min_age_limit = 45
                

            #     reply = cowin.driver(pincode,date,min_age_limit)             
            # except:
            #     reply= "Please put your query in given format"
            
            pincode = l[1]
            # date = l[2]
            min_age_limit = 45
                


            reply = cowin.driver(pincode)
            # print(reply[10])
            try:
                msg.body(reply[:699])
            except:
                msg.body(reply)
            responded=True
            completionMsg=reply
    if 'covidinfo' in incoming_msg:
        l= incoming_msg.split()
        state = 'india'
        if(len(l)>1):
            state=""
            for i in l[1:]:
                state+= i+" "
            state=state[:-1]
        c,r,d,a = statistics.driver(state)
        reply = "\n✅Confirmed: "+ str(c) +"\n✅Recovered: "+str(r)+"\n✅Active: "+str(a)+"\n✅Deceased: "+str(d)
        msg.body(reply)
        responded=True
        completionMsg=reply
    if 'contact' in incoming_msg:
        reply= "Hi I am Gauransh Soni\nSophomore @ IIT Delhi\nEmail - picografix@gmail.com\nContact No. 9462447291"
        msg.body(reply)
        responded=True
        completionMsg=reply
    if 'task' in incoming_msg:
        reply = "Here is a list of items I can do\n1)Type 'covidhelp <cityname> <Oxygen or Remedesivir or Plasma>' to get recent leads for asked item\n2)Type 'covidinfo <state>' to get recent statistics of covid cases in your state\n3)Type 'emergency <pincode>' to get the contact number of emergency services in your area\n4)Type 'covidvaccine <pincode>' to check availability of vaccine in your area\n5)Type 'help' to get more info"
        msg.body(reply)
        responded=True
        completionMsg=reply
    
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
        completionMsg = quote
    if 'aurbhai' in incoming_msg:
        # return a cat pic
        msg.body('I love cats')
        msg.media('https://cataas.com/cat')
        responded = True
        completionMsg = 'https://cataas.com/cat'
    if 'wallpaper' in incoming_msg:
        l=incoming_message.split()
        url=l[1]
        try: 
            from googlesearch import search 
        except ImportError:  
            print("No module named 'google' found") 
            completionMsg = "No module named 'google' found"
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
        completionMsg=alink
        responded=True
    if 'unsplash' in incoming_msg:
         # return a cat pic
        msg.body('Here You Go ')
        un_img = 'https://source.unsplash.com/random'
        msg.media(un_img)
        responded = True
        completionMsg = un_img
    if 'spam' in incoming_msg:
         # spams 
        l = incoming_msg.split()
        countSpam = int(l[1])
        mess = " ".join(l[2:])
        for i in range(countSpam):
            msg.body(mess)
        completionMsg = "Succesfully spammed"
        responded = True
    if 'dank-joke' in incoming_msg:
        #sends a random dank joke
        responseDog=requests.get("https://sv443.net/jokeapi/v2/joke/Any?type=single")
        l = responseDog.json()
        msg.body(l['joke'])
        completionMsg = l['joke']
        responded = True
    if 'dict' in incoming_msg:
        headersDict = {    'Authorization': 'Token e3d0b4298a9592eb23efa0419b031d2ffadc94d4',
            }
        urlForDict = 'https://owlbot.info/api/v4/dictionary/'
        incoming_msg = 'dict cat'
        l = incoming_msg.split()
        searchTerm = l[1]
        urlForDict += searchTerm
        response = requests.get(urlForDict, headers=headersDict)
        ans = response.json()
        pronounciation = ans['pronunciation']
        defination = ans['definitions'][0]['definition']
        img = ans['definitions'][0]['image_url']
        example = ans['definitions'][0]['example']
        returnString = "*Defination* : " + defination + "\n" + "*usage*: " + example
        msg.body(returnString)
        msg.media(img)  
        completionMsg="successfully sent"
        responded = True
    if 'que' in incoming_msg:
        import urllib.request, urllib.parse, urllib.error
        import xml.etree.ElementTree as ET
        import ssl
        from bs4 import BeautifulSoup as bs

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = ' '.join(incoming_msg.split()[1:])

        try: 
            from googlesearch import search 
        except ImportError:  
            print("No module named 'google' found") 
          
        # to search 
        query = url+" stackoverflow"
          
        for j in search(query, tld="co.in", num=1, stop=1, pause=2): 
            url=j 
        a=urllib.request.urlopen(url,context=ctx).read()
        soup=bs(a,'html.parser')
        L=soup.find_all('div',{'class':'post-text'})
        i=L[1]
        msg.body(i.text)
        print(i.text)
        completionMsg = i.text
        responded = True
    
    if not responded:
        msg.body('type bothelp')
        completionMsg ="Job Done"
    row = [current,incoming_num1[9:],incoming_num2[9:],incoming_msg,completionMsg]
    f = open("output.txt", "a")
    if incoming_msg!="":
        myadd=""
        for string in row:
            myadd+= string+" "
        f.write(myadd+"\n")
        f.close()
    # sheet.insert_row(row,index=2)
    return str(resp)

@app.route('/')
def index():
    return "hello this is my whatsapp bot"
if __name__ == '__main__':
    app.run()
