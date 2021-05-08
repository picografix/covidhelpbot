from twilio.rest import Client 
from config import account_sid,auth_token
 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='please code for me :)',      
                              to='whatsapp:+918279756297' 
                          ) 
 
print(message.sid)