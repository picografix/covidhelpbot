import requests, os
# from discord.ext import commands
# from dotenv import load_dotenv
from bs4 import BeautifulSoup
session = requests.Session()
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
def chegg( arg):

        if "https://www.chegg.com/homework-help/" not in arg: 
            print("not a chegg link")
            return
        else:
            

            
            page = session.get(arg,headers=headers)
            pageContent = page.content
            soup = BeautifulSoup(pageContent,"html.parser")
            
            answerDiv = soup.find("div",{"class":"answer-given-body ugc-base"})
            # answerImages = answerDiv.findAll('img')
            answerText = answerDiv.getText()


        
            for image in answerImages:
                # await ctx.author.send(image['src'])
                print(image['src'])

            if(not answerText):
                return

            # await ctx.author.send('#######################################')
            


            file = open('answer.txt', 'w')
            file.write(answerText)
            file.close()
            # my_files = [discord.File('answer.txt')]
            # await ctx.author.send(files=my_files)



arg= "https://www.chegg.com/homework-help/questions-and-answers/define-random-variable-q6521141"
chegg(arg)