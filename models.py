from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import db

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80))

class Words(db.Model):
    __tablename__ = 'Words'
    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(15), unique=True)
    definition = db.Column(db.String(120))
    added_by_user_id = db.Column(db.Integer)

class Synonyms(db.Model):
    __tablename__ ='Synonyms'
    synonym_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word_id = db.Column(db.Integer)
    synonym = db.Column(db.Integer, server_default="none")