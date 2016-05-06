# send a testing message to phone
from twilio.rest import TwilioRestClient
from EthiopiaSMS.config import *


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def send_message(body, to_number):
  message = client.messages.create(
    from_= FROM_NUMBER,
    to = TO_NUMBER,
    body = "Test test hello"
    )
  # function will log this into a database
  print (message.sid)
