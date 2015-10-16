# send a testing message to phone
from twilio.rest import TwilioRestClient
from config import *

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages.create(
  from_= FROM_NUMBER,
  to = TO_NUMBER,
  body = "Test test hello" 
  )
print message.sid
