from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1635922:differentPassword98@csmysql.cs.cf.ac.uk:3306/c1635922_flask_blog'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
from blog import routes

from flask_admin import Admin
from blog.models import User, Post, Comment, Vote, Fave
from blog.views import AdminView
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))
admin.add_view(AdminView(Vote, db.session))
admin.add_view(AdminView(Fave, db.session))

