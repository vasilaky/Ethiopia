# EthiopiaSMS

## Organization/Directory Structure
```
.
├── README.md         # This will be how to test/run the app & have basic info
├── requirements.txt  # These are the dependencies that you need to install for the app to run
├── run.py            # Runs the app!
├──  app/             # Everything our app includes is inside this folder
│   ├──  __init__.py  # App-wide setup. Called by `run.py`
│   ├──  config.py    # Configuration Files. i.e. Login related things
│   ├──  views.py     # All the view routes
│   ├──  data/        # Folder for any data we might want to use
│   ├──  scripts/     # Folder for any scripts for the database we add
│   ├──  static/      # Folder for any static files
│   │   ├──  css      # CSS
│   │   ├──  images   # Images
│   │   ├──  js       # JavaScript
│   ├──  templates/   # HTML files go here
```
