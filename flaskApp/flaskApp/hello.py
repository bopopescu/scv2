# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request,json
from flask_sqlalchemy import SQLAlchemy
import string
from datetime import datetime,timedelta
from orm.func import *
from orm.model import *
import datetime

import os
from flask import Flask, render_template_string,render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
#from orm.user import User
from orm.model import User
from orm.model import db

# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'mysql+mysqlconnector://scv2:scv2@localhost/scv2db')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'gros.brother@gmail.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'scv2power8000')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"SCV2" <gros.brother@gmail.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = "Sens Critique V2"                # Used by email templates
    

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config.from_object(__name__+'.ConfigClass')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()
mail = Mail(app)                                # Initialize Flask-Mail

db.create_all()

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
    
@app.route('/login')
def home_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Home page</h2>
            <p>This page can be accessed by anyone.</p><br/>
            <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
            <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
        {% endblock %}
        """)

# The Members page is only accessible to authenticated users
@app.route('/members')
@login_required                                 # Use of @login_required decorator
def members_page():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Members page</h2>
            <p>This page can only be accessed by authenticated users.</p><br/>
            <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
            <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
        {% endblock %}
        """)


@app.route('/look')
def show_entries():
    cur = db.Query('select type_name,firstname,lastname,participant_id from participant order by participant_id desc')
    entries = cur
    return render_template('pages/menu.html', participants=entries)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('/'))
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('/'))

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/signUp')
def signUp():
    return render_template('login.html')

@app.route('/items')
def f():
    return render_template('pages/rank.html')

@app.route('/item')
def item():
    return render_template('pages/item.html')

@app.route('/')
def index():
    return render_template('pages/menu.html')#pages/menu.html


if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run()
