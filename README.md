# EthiopiaSMS
### How to Set Up For the First Time
1) Create an `.env` file with all the variables from the `config.py` file defined. The structure is as follows:
   ```
  export TO_NUMBER="[Actual Phone Number]"
  export FROM_NUMBER="[Actual Phone Number]"
  export ACCOUNT_SID="[Our Twilio Account SID]"
  export AUTH_TOKEN="[Our Twilio Auth Token]"
  export DATABASE_URL="[Database_Url]"
  ```

2) Type `source .env` to upload your environment variables into local memory.

3) Install all the dependencies we currently have with `pip install -r requirements.txt`
- If you don't want the dependencies installed locally you can create a virtual machine by:
- `pip install virtualenv`
- `virtualenv venv`
- `source venv/bin/activate`
- Then install all the requirements! with `pip install -r requirements.txt`

### How to Run the Application
1) Run the app with `python run.py`

## Organization/Directory Structure
```
.
├── .gitignore            # So that we don't commit compiled files or our environment passwords
├── README.md             # This will be how to test/run the app & have basic info
├── requirements.txt      # These are the dependencies that you need to install for the app to run
├── run.py                # Runs the app!
├──  app/                 # Everything our app includes is inside this folder
│   ├──  __init__.py      # App-wide setup. Called by `run.py`
│   ├──  config.py        # Configuration Files. i.e. Login related things
│   ├──  views.py         # All the view routes
│   ├──  data/            # Folder for any data we might want to use
│   ├──  scripts/         # Folder for any scripts for the database we add
│   ├──  static/          # Folder for any static files
│   │   ├──  css          # CSS
│   │   ├──  images       # Images
│   │   ├──  js           # JavaScript
│   ├──  templates/       # HTML files go here
│   │   ├──  index.html   # JavaScript
```
