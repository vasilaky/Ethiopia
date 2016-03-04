from EthiopiaSMS import app
import os

port = int(os.environ.get('PORT', 8000))
app.run(port=port,debug=True)
