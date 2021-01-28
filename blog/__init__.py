from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1635922:differentPassword98@csmysql.cs.cf.ac.uk:3306/c1635922_flask_blog'
db = SQLAlchemy(app)

from blog import routes