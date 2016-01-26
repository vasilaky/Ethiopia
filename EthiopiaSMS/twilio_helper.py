# send a testing message to phone
from twilio.rest import TwilioRestClient
from config import *

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


def send_call(to_number):
    fallback_url = ("http://twimlets.com/holdmusic"
                    "?Bucket=com.twilio.music.ambient")

    call = client.calls.create(
        from_=FROM_NUMBER,
        to=to_number,
        url=fallback_url
    )

    return call.sid


def get_call_logs():
    return client.calls.list()


def get_logs_csv():
    csv_request_url = ('https://api.twilio.com/2010-04-01/Accounts/{}'
                       '/Calls.csv').format(ACCOUNT_SID)
    return csv_request_url