from twilio.rest import Client 
 
account_sid = 'ACaa40d5fd76e3d54bdde5807fce65adbb' 
auth_token = 'a67f9ecae87624705b59b7816361cf05' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='hurrr',      
                              to='whatsapp:+919166204789' 
                          ) 
 
print(message.sid)