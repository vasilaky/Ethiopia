# send a testing message to phone
from twilio.rest import TwilioRestClient

account_sid = "AC22f356962448e8d1dec923f73a6e3c32"
auth_token = "718b076489a5cfd9646b3d1e198f7ab1"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
  from_= "+19175384134",
  to = "315-796-8749",
  body = "Test test hello" 
  )
print message.sid
