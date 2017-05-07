from flask import Flask, jsonify, render_template, request,json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flaskApp.scv2func import *
import string

app2 = Flask(__name__)  # Construct an instance of Flask class for our webapp
db = SQLAlchemy()

scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')
metadata = MetaData(scv2_engine)
tables = importContext(scv2_engine,metadata)
item = tables['item']

conn = scv2_engine.connect()


@app2.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app2.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app2.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    if user=='Thomas':
        return 'yes'
    else:
        return 'no'    
    #return json.dumps({'status':'OK','user':user,'pass':password});
    
@app2.route('/f')
def f():
    return render_template('pages/Films/Films/film_page1.html')

@app2.route('/m')
def m():
    return render_template('pages/menu.html')

@app2.route('/clever')
def clever():
    return render_template('pages/menu.html',clever=1)

@app2.route('/')
def index():
    return render_template('pages/menu.html')#pages/menu.html

if __name__ == '__main__':
    app2.config['SQLALCHEMY_ECHO'] = True
    app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app2.debug = True
    print("\n\n\n\nYOOOO\n\n")
    app2.run()