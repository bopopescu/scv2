# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app2 = Flask(__name__) 
app2.config.from_object(__name__) # load config from this file , flaskr.py

#nvironment variable FLASKAPP_SETTINGS that points to a config file to be loade
app2.config.from_envvar('FLASKAPP_SETTINGS', silent=True)
db = SQLAlchemy()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    