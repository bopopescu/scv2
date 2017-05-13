# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request,json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
from datetime import datetime,timedelta
from scv2_ORM.rqst_func_scv2 import *
from scv2_ORM.base_model_scv2 import *
import datetime

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()
db.create_all()

#ALWAYS KEEP TYPESLIST IN render_template!!!

@app.route('/')
def redir_home():
	return redirect(url_for('home'))
	
@app.route('/home')
def home():
	return render_template('pages/home.html', typeslist=db.session.query(Itemtype).all())

@app.route('/All')
def itemlist_All_alphabetic():
	res_all_items = db.session.query(Item).order_by(Item.title).all()
	return render_template('pages/all_items.html', typeslist=db.session.query(Itemtype).all(), all_items = res_all_items, filter_requested = "Alphabetic order", my_itemtypename = "TYPE A AFFICHER...")

@app.route('/All/<myfilter>')
def itemlist_All_sorted(myfilter):
	if myfilter == "Best":
		return render_template('pages/all_items.html', typeslist=db.session.query(Itemtype).all(), all_items =db.session.query(Item).order_by(Item.mean.desc()).all(), filter_requested = myfilter )
	if myfilter == "Recent":
		return render_template('pages/all_items.html', typeslist=db.session.query(Itemtype).all(), all_items =db.session.query(Item).order_by(Item.release_date.desc()).all(), filter_requested = myfilter )
	if myfilter == "Famous":
		#return render_template('pages/all_items.html', typeslist=db.session.query(Itemtype).all(), all_items =db.session.query(Item).order_by(MOSTREVIEWEDITEM).all() , filter_requested = myfilter )
		return "Not working yet."
		
@app.route('/<itemtype_name>/<myfilter>')
def itemlist_Types(itemtype_name,myfilter):
	my_item_type = getIdOfItemtype(db.session,Itemtype,itemtype_name)
	if myfilter == "All":
		return render_template('pages/requested_list.html', typeslist=db.session.query(Itemtype).all(), type_requested = itemtype_name, list_requested= db.session.query(Item).filter(Item.type_id == my_item_type).order_by(Item.title).all())
	if myfilter == "Best":
		return render_template('pages/requested_list.html', typeslist=db.session.query(Itemtype).all(), type_requested = itemtype_name, list_requested= db.session.query(Item).filter(Item.type_id == my_item_type).order_by(Item.mean.desc()).all())
	if myfilter == "Recent":
		return render_template('pages/requested_list.html', typeslist=db.session.query(Itemtype).all(), type_requested = itemtype_name, list_requested= db.session.query(Item).filter(Item.type_id == my_item_type).order_by(Item.release_date.desc()).all())
	if myfilter == "Famous":
		#return render_template('pages/requested_list.html', typeslist=db.session.query(Itemtype).all(), type_requested = itemtype_name, list_requested= db.session.query(Item).filter(Item.type_id == my_item_type.item_type_id).order_by(MOSTREVIEWEDITEM).all())
		return "Not working yet."
		
@app.route('/<int:myitemtypeID>/<myItemName>')
def description_Item(myitemtypeID,myItemName):
	realItemName = myItemName.replace("_"," ")
	my_item_ID = getItemID(db.session, Item, myitemtypeID,realItemName)
	itemFields = "Ceci contiendra les champs du item dont l'ID est connu"
	return render_template('pages/pres_item.html',typeslist=db.session.query(Itemtype).all(),myItem = itemFields)

'''
@app.route('/<int:type_id>/<title>')
def item_only(title,type_id):
    return render_template('pages/menu.html',item= 'title+"  "+{0}'.format(str(type_id)))
    
@app.route('/chefs')
def admin():
    return render_template('admin.html',itemtypes=Itemtype.query.order_by(Itemtype.item_type_id).all())

@app.route('/chefs/<int:typeid>')
def adminItem(typeid):
    mytitle = request.args.get('t', 0, type=string)
    mydate = request.args.get('rd', 0, type=string)#24052010
    des = request.args.get('des', 0, type=string)
#!!! ARNO FAIT EN SORTE QUE ÇA MARCHE
    new = Item(title=mytitle)#,type_id=typeid,release_date=datetime.datetime.strptime(mydate,"%d%m%y").date())
    dbAdd(db.session,new)
    db.session.commit()
    return render_template('admin.html')

@app.route('/all')
def allItems():
    results = Item.query.all()
    return render_template('pages/menu.html', entries=results)


@app.route('/search')
def search():
    entries = getItemWithKeyWord(conn,"babar")
    return render_template('pages/menu.html', entries=entries)

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
'''

if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run()
