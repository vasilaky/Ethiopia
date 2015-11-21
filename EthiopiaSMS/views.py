from EthiopiaSMS import app
from flask import render_template, request, redirect, g, url_for
#from config import *
from twilio.rest import TwilioRestClient
from config import *
from database_helper import *
from twilio_helper import *
from datetime import date

user_list = None
call_list = None

@app.route("/", methods=["GET","POST"])
def index():
  if request.method == "POST":

    # If they click the button to send a text message
    cell_number = request.form.get("cell_phone", None)
    text_message = request.form.get("text_message", None)

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
  ####################
  # For adding a new person into our database
  ####################
  cell_phone = request.form.get("cell_phone", None)
  name = request.form.get("name", None)
  
  user_entry = {
  "name": name,
  "cell_phone": cell_phone
  }

  # only add if all the fields are filled out
  if name != None:
    add_user(user_entry)

  # Get all of the current users, updated from the database
  user_list = get_all_users()
  call_list = get_call_logs()
    

  return render_template("users.html", user_list=user_list, call_list=call_list)

@app.route("/send_call_route", methods=["POST", "GET"])
def send_call_route():
    ####################
    # For sending to a list of people selected on our front end
    ####################

    # Get list of user IDs from the selected names
    to_send = request.form.getlist("send", None)
    # Searches from our DB for each user ID and sends to this list of IDs
    to_delete = request.form.getlist("delete", None)
    send_to_list(get_user_info_from_id_list(to_send))
    users = get_user_info_from_id_list(to_delete)
    for user in users:
      delete_user(user)

    #Check Status of call

    # Get all of the current users, updated from the database
    user_list = get_all_users()
    call_list = get_call_logs()

    return redirect(url_for('users'))

def send_to_list(database_users):

  for user_entry in database_users:
    send_call(user_entry['cell_phone'])

@app.route("/get_csv", methods=["POST"])
def foo():
  page = get_logs_csv()
  return redirect(page)

@app.route("/calls", methods=["GET", "POST"])
def calls():
  call_list = get_call_logs()
  return render_template("calls.html", call_list=call_list)