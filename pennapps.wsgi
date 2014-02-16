import sys
import logging
logging.basicConfig(stream=sys.stderr)
file_handler = logging.FileHandler(filename='/tmp/election_error.log')
file_handler.setLevel(logging.WARNING)
sys.path.insert(0,"/var/www/pennapps/")
activate_this = '/var/www/pennapps/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from app import app
app.logger.addHandler(file_handler)
from werkzeug.debug import DebuggedApplication 
application = DebuggedApplication(app, evalex=True)
