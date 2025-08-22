from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__, static_folder='static') # <--- Change this line
app.config['SECRET_KEY'] = 'a-very-secret-key-that-you-should-change'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)

from app import routes, models
