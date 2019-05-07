from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import *
from config import *
from forms import *
from sql import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['POST', 'GET'])
def index():
    return xindex()


@app.route('/addword', methods=['POST', 'GET'])
@login_required
def addword():
    return xaddword()


@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    return xdashboard()


@app.route('/register', methods=['POST', 'GET'])
def register():
    return xregister()


@app.route('/info', methods=['POST', 'GET'])
@login_required
def info():
    return xinfo()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))