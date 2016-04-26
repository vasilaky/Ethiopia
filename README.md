# EthiopiaSMS
### How to Set Up For the First Time
1) Create an `.env` file with all the variables from the `config.py` file defined. All of the actual values are in the heroku account. The structure is as follows:
   ```
  export FROM_NUMBER_SA="[Actual Phone Number, SOUTH AFRICAN]"
  export FROM_NUMBER_DR="[Actual Phone Number, DOMINICAN REPUBLIC]"
  export ACCOUNT_SID="[Our Twilio Account SID]"
  export AUTH_TOKEN="[Our Twilio Auth Token]"
  export DATABASE_URL="[Database_Url]"
  export USERNAME="[In Heroku Settings]"
  export PASSWORD="[In Heroku Settings]"
  ```

2) Type `source .env` to upload your environment variables into local memory.

3) Install all the dependencies we currently have with `pip install -r requirements.txt`
- If you don't want the dependencies installed locally you can create a virtual machine by:
- `pip install virtualenv`
- `virtualenv venv`
- `source venv/bin/activate`
- Then install all the requirements! with `pip install -r requirements.txt`

### How to Run the Application
1) Uncomment the following lines from `run.py` only when you're running locally. If you uncomment them before deploying to github, the site will not work.
```
  # port = int(os.environ.get('PORT', 13336))
  # app.run(port=port,debug=True)
```

2) Run the app with `python run.py`

## Organization/Directory Structure
```
.
├── .gitignore              # So that we don't commit compiled files or our environment passwords
├── README.md               # This will be how to test/run the app & have basic info
├── requirements.txt        # These are the dependencies that you need to install for the app to run
├── run.py                  # Runs the app!
├──  EthiopiaSMS/           # Everything our app includes is inside this folder
│   ├──  __init__.py        # App-wide setup. Called by `run.py`
│   ├──  config.py          # Configuration Files. i.e. Login related things
│   ├──  views.py           # All the view routes
│   ├──  twilio_helper.py   # Twilio Fetching Related functions
│   ├──  database_helper.py # All the view routes
│   ├──  data/              # Folder for any data we might want to use
│   ├──  scripts/           # Folder for any scripts for the database we add
│   ├──  static/            # Folder for any static files
│   │   ├──  css            # CSS
│   │   ├──  images         # Images
│   │   ├──  js             # JavaScript
│   ├──  templates/         # HTML files go here
│   │   ├──  index.html     # JavaScript
```
