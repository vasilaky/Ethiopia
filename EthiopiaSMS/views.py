from EthiopiaSMS import app
from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename
from flask.ext.basicauth import BasicAuth
from twilio.rest import TwilioRestClient
import subprocess
from config import *
from database_helper import *
from twilio_helper import *
import datetime
import json
import time

user_list = None
call_list = None
ethiopia_info = {
    "regions": ["Afar", "Amhara"],
    "villages": [],
    "message": ""
}
app.config['BASIC_AUTH_USERNAME'] = USERNAME
app.config['BASIC_AUTH_PASSWORD'] = PASSWORD

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

basic_auth = BasicAuth(app)

# @app.route('/secret')
# @basic_auth.required
# def secret_view():
#     return render_template('secret.html')

def allowed_file(filename):
    return '.' in filename

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # If they click the button to send a text message
        cell_number = request.form.get("cell_phone", None)

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

@app.route("/record_message", methods =["GET", "POST"])
def record():
  listofsounds = []
  if request.method == "POST":
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      print os.path
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('uploaded_file',
                              filename=filename))
  return render_template("record.html", listofsounds=listofsounds)


def check_user(user_entry):
    # simple check on user info
    if user_entry["name"] == None or user_entry["cell_phone"] == None or \
    user_entry["region"] == None or user_entry["village"] == None:
        return False
    for name_part in user_entry["name"].split(" "):
        if not name_part.isalpha():
            return False
    if not user_entry["cell_phone"].isnumeric():
        return False
    for region_part in user_entry["region"].split(" "):
        if not region_part.isalpha():
            return False
    for village_part in user_entry["village"].split(" "):
        if not village_part.isalpha():
            return False
    return True


@app.route("/users", methods=["GET", "POST"])
# @basic_auth.required
def users():
    date = datetime.datetime.utcnow()
    date = date + datetime.timedelta(hours=3)
    date = date.strftime("%a %I:%M%p %d %B %Y")
    ethiopia_info["time_string"] = date

    if request.method == "POST":
        ####################
        # For adding a new person into our database
        ####################
        cell_phone = request.form.get("cell_phone", None)
        name = request.form.get("name", None)
        input_region = request.form.get("regions", None)
        input_village = request.form.get("villages", None)

        user_entry = {
            "name": name,
            "cell_phone": cell_phone,
            "region": input_region,
            "village": input_village
        }

        # only add if passed checking
        if check_user(user_entry):
            # add region number to phone number
            if user_entry["region"] == "United States":
                if not user_entry["cell_phone"].startswith("1"):
                    user_entry["cell_phone"] = "1" + str(user_entry["cell_phone"])
            elif user_entry["region"] == "Ethiopia":
                if not user_entry["cell_phone"].startswith("251"):
                    user_entry["cell_phone"] = "251" + str(user_entry["cell_phone"])
            else:
                print("Not supported")

            # add user to db
            add_user(user_entry)
        else:
            # did not fill all required fields
            print("counld not add user.")

    # Get all of the current users, updated from the database
    user_list = get_all_users()
    call_list = get_call_logs()

    return render_template(
        "users.html", user_list=user_list, call_list=call_list,
        ethiopia_info=ethiopia_info)


@app.route("/send_call_route", methods=["POST", "GET"])
def send_call_route():

    # For doing actions to a list of people selected on our front end
    option = request.form["options"]
    selected = request.form.getlist("select", None)
    if (option == "voice"):
        send_to_list(get_user_info_from_id_list(selected))
    elif (option == "delete"):
        users = get_user_info_from_id_list(selected)
        for user in users:
            delete_user(user)
    elif (option == "sms"):
        sms_text = request.form["question"]
        ethiopia_info['message'] = sms_text
        print sms_text
    else:
        print("This should not be reached.")

    '''
    Get all of the current users, updated from the database
    user_list = get_all_users()
    call_list = get_call_logs()
    '''

    # Check Status of call

    return redirect(url_for('users'))


def send_to_list(database_users):
    # TWO Important functions: Adds call to db & sends call
    for user_entry in database_users:
        call_id = send_call(user_entry['cell_phone'])
        add_call_to_db(user_entry['id'], call_id)


@app.route("/get_csv", methods=["POST"])
def foo():
    page = get_logs_csv()
    return redirect(page)


@app.route("/calls", methods=["GET", "POST"])
def calls():
    call_list = get_call_logs()
    return render_template("calls.html", call_list=call_list)

@app.route("/smssynch", methods=["GET", "POST"])
def synch():
    # http://ethiopia-sms.herokuapp.com/smssynch?task=send&secret=bschool
    task = request.args.get('task')
    ts = datetime.datetime.strftime('+%Y-%m-%d %H:%M:%S UTC')
    # ts = 'uniquesym'
    # print request.get_json()
    # time.sleep(300)
    if task == 'send':
      print "send task"
      print task
      # print request.get_json()
      message = ethiopia_info.get('message')
      print message
      return '''{"payload": {
                  "success": "true",
                  "error": null,
                  "secret": "bschool",
                  "task": "send",
                  "messages": [{
                    "to": "+17149075336",
                    "message": "%s",
                    "uuid": "%s"}]
                  }
                  }''' % (message, str(ts))
    if task == 'sent':
      print "sent task"
      print task
      print request.get_json()
      messages_response = request.get_json()
      messages = messages_response.get('queued_messages')
      return '''{"message_uuids" : %s}''' % (messages)
    else:
      message = ethiopia_info.get('message')
      print "print other task (should send msg to phone)"
      print message
      print task
      # print request.get_json()
      return '''{"payload": {
                  "success": "true",
                  "error": null,
                  "secret": "bschool",
                  "task": "send",
                  "messages": [{
                    "to": "+17149075336",
                    "message": "hello world",
                    "uuid": "%s"}]
                  }
                }''' % (str(ts))

@app.route("/xml", methods=["GET", "POST"])
def return_xml():
  xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman" language="en-US">Hello Welcome to Ethiopia SMS!</Say>
  <Play loop="5">https://api.twilio.com/cowbell.mp3</Play>
    <Gather timeout="10" finishOnKey="*">
        <Say>Did it rain yesterday? Press 1 for Yes. Press 0 for No</Say>
    </Gather>
</Response>"""
  return xml

@app.route("/send_text", methods=["GET", "POST"])
def send_text():
  return render_template("messages.html")

@app.route("/scripts/<path:path>", methods=["GET","POST"])
def work(path):
  return send_from_directory('scripts', path)

@app.route("/twiml")
def sounds():
  return '''<?xml version="1.0" encoding="UTF-8"?>
<Response><Play>http://com.twilio.music.ambient.s3.amazonaws.com/aerosolspray_-_Living_Taciturn.mp3</Play><Play>http://com.twilio.music.ambient.s3.amazonaws.com/gurdonark_-_Plains.mp3</Play><Play>http://com.twilio.music.ambient.s3.amazonaws.com/gurdonark_-_Exurb.mp3</Play><Redirect/></Response>'''

