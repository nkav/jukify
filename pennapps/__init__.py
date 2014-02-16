from flask import Flask
from settings import SECRET_KEY, SQLALCHEMY, UPLOAD_FOLDER, STATIC_FOLDER
 
app = Flask(__name__)
app.secret_key = SECRET_KEY 

# Flask-SQLAlchemy Settings 
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY 

#File Upload Settings
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['STATIC_FOLDER'] = STATIC_FOLDER 

#Initialize App with DB and Email
from models import db
db.init_app(app)

#import urls
import routes

#INitialize Flask-Admin
from admin import MyHomeView
from flask.ext.admin import Admin 
from flask.ext.admin.contrib.sqla import ModelView
from models import Member
admin = Admin(app, index_view=MyHomeView(), name="PennApps-S14 Admin")
admin.add_view(ModelView(Member, db.session))
