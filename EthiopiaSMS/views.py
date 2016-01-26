from EthiopiaSMS import app
from flask import render_template, request, redirect, url_for, send_from_directory
from flask.ext.basicauth import BasicAuth
from twilio.rest import TwilioRestClient
import subprocess
from config import *
from database_helper import *
from twilio_helper import *
import datetime

user_list = None
call_list = None
ethiopia_info = {
    "regions": ["Afar", "Amhara"],
    "villages": []
}
app.config['BASIC_AUTH_USERNAME'] = 'eunice'
app.config['BASIC_AUTH_PASSWORD'] = '2016E'

basic_auth = BasicAuth(app)

# @app.route('/secret')
# @basic_auth.required
# def secret_view():
#     return render_template('secret.html')


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


@app.route("/users", methods=["GET", "POST"])
@basic_auth.required
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

        if not cell_phone.startswith("251"):
            cell_phone = "1" + str(cell_phone)

        user_entry = {
            "name": name,
            "cell_phone": cell_phone,
            "region": input_region,
            "village": input_village
        }

        # only add if all the fields are filled out
        if cell_phone:
            add_user(user_entry)

    # Get all of the current users, updated from the database
    user_list = get_all_users()
    call_list = get_call_logs()

    return render_template(
        "users.html", user_list=user_list, call_list=call_list,
        ethiopia_info=ethiopia_info)


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

@app.route("/send_text", methods=["GET", "POST"])
def send_text():
  return render_template("messages.html")

@app.route("/scripts/<path:path>", methods=["GET","POST"])
def work(path):
  return send_from_directory('scripts', path)
