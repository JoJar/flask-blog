from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1635922:differentPassword98@csmysql.cs.cf.ac.uk:3306/c1635922_flask_blog'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


app.config['SECRET_KEY'] = os.urandom(24).hex()

from blog import routes