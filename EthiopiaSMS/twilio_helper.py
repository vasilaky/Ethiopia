# send a testing message to phone
from twilio.rest import TwilioRestClient
from config import *


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def send_message(body, to_number):
  message = client.calls.create(
    from_= FROM_NUMBER,
    to = to_number,
    url = "http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient" 
    )
  # function will log this into a database
  print message.sid
