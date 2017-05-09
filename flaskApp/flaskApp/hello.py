# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request,json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import sqlalchemy

from scv2_initfunc import *
from scv2_rqstfunc import *
import string
from datetime import datetime,timedelta

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
db = SQLAlchemy()

scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')
metadata = MetaData(scv2_engine)


conn = scv2_engine.connect()

@app.route('/all')
def allItems():
    results = getAllItems(conn)
    return render_template('pages/menu.html', entries=results)


@app.route('/search')
def search():
    entries = getItemWithKeyWord(conn,"babar")
    return render_template('pages/menu.html', entries=entries)

@app.route('/look')
def show_entries():
    cur = conn.execute('select type_name,firstname,lastname,participant_id from participant order by participant_id desc')
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
    return render_template('signUp.html')

@app.route('/f')
def f():
    return render_template('pages/Films/Films/film_page1.html')

@app.route('/item')
def item():
    return render_template('pages/Films/Films/Harry_Potter.html')

@app.route('/m')
def m():
    return render_template('pages/menu.html',bod="<h1>cool</h1>")

@app.route('/clever')
def clever():
    print(' \n\n\n Menu ! \n\n\n')
    return render_template('pages/menu.html',clever=1)

@app.route('/')
def index():
    return render_template('pages/menu.html')#pages/menu.html

if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run()
