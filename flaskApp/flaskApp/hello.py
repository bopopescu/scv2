from flask import Flask, jsonify, render_template, request,json
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


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    if user=='Thomas':
        return 'yes'
    else:
        return 'no'    
    #return json.dumps({'status':'OK','user':user,'pass':password});
    
@app.route('/f')
def f():
    print(' \n\n\n Ciné !\n\n\n')
    return render_template('pages/Films/Films/film_page1.html')

@app.route('/m')
def m():
    print(' \n\n\n Menu ! \n\n\n')
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