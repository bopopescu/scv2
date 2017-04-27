from flask import Flask, render_template, redirect, url_for  # From 'flask' module import 'Flask' class
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import *
from scv2func import *
import string

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
db = SQLAlchemy()

scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')
metadata = MetaData(scv2_engine)
tables = importContext(scv2_engine,metadata)
item = tables['item']

conn = scv2_engine.connect()

@app.route('/')
def main():
    return render_template('index.html', titles=conn.execute(select([item.c.title])))

if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run()
