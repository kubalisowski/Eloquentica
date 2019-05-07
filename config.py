from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

class Config(object):
    app.config['SECRET_KEY'] = 'f5f4a01b-1331-439d-89f0-586dccf1d992'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'