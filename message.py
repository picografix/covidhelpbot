from twilio.rest import Client 
from config import account_sid,auth_token
 
client = Client(account_sid, auth_token) 
 
# message = client.messages.create( 
#                               from_='whatsapp:+14155238886',  
#                               body='please code for me :)',      
#                               to='whatsapp:+918279756297' 
#                           ) 
 

def send(incoming,body,media):
    client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=body,
                              media_url=media,      
                              to=incoming 
                          )
# print(message.sid)
# send('whatsapp:+918279756297','helllo',['https://demo.twilio.com/owl.png'])