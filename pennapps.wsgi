import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/pennapps/")
activate_this = '/var/www/pennapps/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from app import app as application
application.debug = True
