from flask import Flask, jsonify, render_template, request, json, redirect, url_for, render_template_string, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

from scv2_ORM.rqst_func_scv2 import *
from scv2_ORM.base_model_scv2 import *

from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import *


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'static/upload/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
class ConfigClass(object):
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'gros.brother@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'scv2power8000')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"SCV2" <gros.brother@gmail.com>')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

    # Flask-User settings
    USER_APP_NAME = "Inscale"  # Used by email templates
    

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config.from_object(__name__ + '.ConfigClass')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()
mail = Mail(app)  # Initialize Flask-Mail

db.create_all()

db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User
    
T = [ truc.name for truc in db.metadata.sorted_tables]  # Table names 

# launch phpmyadmin: systemctl restart httpd

##########################  USEFUL FOR FIXED SIDEBARS
res_all_itemtypes = mainheader(db.session, Item, Itemtype, Participation)
##########################   END FOR SIDEBARS
####### NEVER FORGET TO PUT IN render_template: typeslist = res_all_itemtypes


####################login here#############################
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

# To display one item
@app.route('/<itemtype_name>/<int:myitemID>/<myItemTitle>')
def description_Item(itemtype_name, myitemID, myItemTitle):
    myItemTitle.replace("_"," ")
    
    myItemObject = db.session.query(Item).filter(Item.item_id == myitemID).one()
    #return str(myItemObject)
    return render_template('pages/item.html', typeslist=res_all_itemtypes, myitem=myItemObject)
 


# To display one add picture item
@app.route('/<itemtype_name>/<int:myitemID>/<myItemTitle>/add', methods=['GET', 'POST'])
def add_picture_Item(itemtype_name, myitemID, myItemTitle):
    myItemTitle.replace("_"," ")
    myItemObject = db.session.query(Item).filter(Item.item_id == myitemID).one()
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # filename="cool"+file.filename.rsplit('.', 1)[1].lower()
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + myItem.__tablename__):
                os.makedirs(app.config['UPLOAD_FOLDER'] + myItem.__tablename__)
            filename = myItem.username + "." + file.filename.split(".")[1]
            print(myItem.__tablename__+"/"+app.config['UPLOAD_FOLDER'] + filename+"\n\n\n\n !!!\n")
            if os.path.isfile(app.config['UPLOAD_FOLDER'] +toto.__tablename__+"/"+ filename+filename+time.strftime("%Y%m%d-%H%M%S")):
                return redirect(url_for('failure'))
            else :
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+toto.__tablename__, filename+time.strftime("%Y%m%d-%H%M%S")))
                return redirect(url_for('success',fileAdd="yes it has been added??"))
    return render_template('pages/item.html', monItem=myItem,add=1)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # filename="cool"+file.filename.rsplit('.', 1)[1].lower()
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + toto.__tablename__):
                os.makedirs(app.config['UPLOAD_FOLDER'] + toto.__tablename__)
            filename = toto.username + "." + file.filename.split(".")[1]
            print(toto.__tablename__+"/"+app.config['UPLOAD_FOLDER'] + filename+"\n\n\n\n !!!\n")
            if os.path.isfile(app.config['UPLOAD_FOLDER'] +toto.__tablename__+"/"+ filename+filename+time.strftime("%Y%m%d-%H%M%S")):
                return redirect(url_for('failure'))
            else :
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+toto.__tablename__, filename+time.strftime("%Y%m%d-%H%M%S")))
                return redirect(url_for('success',fileAdd="yes it has been added??"))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/a')
def AllTypesWithRoles():
	return str(res_all_itemtypes)

@app.route('/')
def home():
	return render_template('pages/home.html', typeslist=res_all_itemtypes)

'''
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
@login_required  # Use of @login_required decorator
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
'''        
####################login ends here#############################


@app.route('/All')
def itemlist_All_alphabetic():
	return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items=getAllItems(db.session, Item, Itemtype), filter_requested="Alphabetic order", displayRoles='no')
	
@app.route('/All/<myfilter>')
def itemlist_All_sorted(myfilter):
	if myfilter == 'Roles':
		a = getAllRoles(db.session, Participation)
		b = [ x[0] for x in a ]
		return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items=b, filter_requested=myfilter, displayRoles='yes')
	else:
		return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items=getAllItems_WithFilter(db.session, Item, Itemtype, myfilter), filter_requested=myfilter, displayRoles='no')

# To display a requested list
@app.route('/<itemtype_name>/<myfilter>')
def itemlist_Types(itemtype_name, myfilter):
	mytypeID = getIdOfItemtype(db.session, Itemtype, itemtype_name)
	
	return render_template('pages/requested_list.html', typeslist=res_all_itemtypes, list_requested=getAllItemsOfThisIDType_WithFilter(db.session, Item, Itemtype, myfilter, mytypeID), filter_requested=myfilter, type_requested=itemtype_name.title())

# #THIS IS DONE TWICE (IF URL /ITEMTYPE or /ITEMTYPE/)
# To display a requested list in alphabetic order
@app.route('/<itemtype_name>')
def itemlist_Types_alphabetic(itemtype_name):
	mytypeID = getIdOfItemtype(db.session, Itemtype, itemtype_name)
	
	if mytypeID > 0:
		redir = '/' + itemtype_name + '/All'
		return redirect(redir)
	else:
		return redirect('/')
        
# To display a requested list in alphabetic order
@app.route('/<itemtype_name>/')
def itemlist_Types_alphabeticBIS(itemtype_name):
	redir = '/' + itemtype_name
	return redirect(redir)


# To display a requested list from keywords
@app.route('/search', methods=['POST'])
def searchByKeywords():
	keyWords = request.form.get('Mysearch')
	mylist = keywordSearch(db.session, Participant, Item, keyWords)
	isAnItem = []
	itemName = []
	temp = ()
	res = ()
	
	# Test if the found object is item: if yes then true
	for each in mylist:
		isAnItem.append(isinstance(each, Item))
	
	temp = list(zip(mylist, isAnItem))
	
	# x: list and y: true (Item) & false (Participant)
	itemName = [db.session.query(Itemtype).filter(Itemtype.item_type_id == x.type_id).one().type_name if y else 'Participant' for (x, y) in temp ]
	
	# (details, item/participant)
	res = list(zip(mylist, itemName))
	
	ParticipantCounter = [db.session.query(Participation).filter(Participation.participant_id == x.participant_id).count() if y == 'Participant' else 0 for (x, y) in res ]
	
	# ((details, item/participant),nbOfItems)
	final_res = list(zip(res, ParticipantCounter))
	
	# return str(final_res)
	return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested=final_res, type_requested="Search results", MyKeywords=keyWords)
	
# if the user is trying to reach /search in the url

@app.route('/search', methods=['GET'])
def search():
	return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested="", type_requested="Search results")



# all roles in ALL TYPES
@app.route('/Roles')
def redirToAllRoles():
	return redirect('/All/Roles')

	

# all roles in ONE GIVE NAME OF ITEM TYPE
@app.route('/<mytypeName>/Roles')
def AllRoles_ItemTypeName(mytypeName):
	mytypeID = getIdOfItemtype(db.session, Itemtype, mytypeName)
	
	if mytypeID > 0:
		rol = getItemtypeIDRoles(db.session, Item, Participation, mytypeID)
			
	return render_template('pages/roles.html', typeslist=res_all_itemtypes, list_requested=rol, filter_requested=myrole, type_requested=mytypeName, ItsARole=-1)

# list of A GIVEN ROLE of A GIVEN TYPE
@app.route('/<mytypeName>/Roles/<myrole>')
def OneRole_ItemTypeName(mytypeName, myrole):
	mytypeID = getIdOfItemtype(db.session, Itemtype, mytypeName)
	rol = getItemtypeIDRoles(db.session, Item, Participation, mytypeID)
	
	WhoHaveThisRole = getWhoHaveThisRole(db.session, Participant, Participation, myrole)
	# return str(WhoHaveThisRole[0].participant_id)
	return render_template('pages/roles.html', typeslist=res_all_itemtypes, list_requested=WhoHaveThisRole, filter_requested=myrole, type_requested=mytypeName, ItsARole=0)



# To display one participant
@app.route('/<mytypeName>/Roles/<int:myparticipantID>/<myparticipantName>')
def description_Participant(mytypeName, myparticipantID, myparticipantName):
	return "ok this is for displaying participant"



# Handling error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/error.html', typeslist=res_all_itemtypes)

if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run()
