from EthiopiaSMS import app
from flask import render_template, request, redirect, g
#from config import *
from twilio.rest import TwilioRestClient
from config import *
from database_helper import *

@app.route("/", methods=["GET","POST"])
def index():
  if request.method == "POST":
    cell_number = request.form.get("cell_phone", None)
    text_message = request.form.get("text_message", None)

    print text_message
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    call = client.calls.create(
      to=cell_number, 
      from_=FROM_NUMBER, 
      url="http://ethiopia-sms.herokuapp.com",  
      method="GET",  
      fallback_method="GET",  
      status_callback_method="GET",    
      record="false"
    ) 
     
    print call.sid

  return render_template("index.html")

@app.route("/users", methods=["GET","POST"])
def users():
  user_list = get_all_users()
  
  if request.method == "POST":
    cell_phone = request.form.get("cell_phone", None)
    name = request.form.get("name", None)
    
    user_entry = {
    "name": name,
    "cell_phone": cell_phone
    }

    add_user(user_entry)
    user_list = get_all_users()

  return render_template("users.html", user_list=user_list)