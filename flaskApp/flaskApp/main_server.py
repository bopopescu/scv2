from flask import Flask, jsonify, render_template, request,json, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
from datetime import datetime,timedelta
from scv2_ORM.rqst_func_scv2 import *
from scv2_ORM.base_model_scv2 import *
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
import os
import datetime


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
    USER_APP_NAME        = "Inscale"                # Used by email templates
    

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config.from_object(__name__+'.ConfigClass')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()
mail = Mail(app)                                # Initialize Flask-Mail

db.create_all()

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
    
T = [ truc.name for truc in db.metadata.sorted_tables]  # Table names 

# launch phpmyadmin: systemctl restart httpd

##########################  USEFUL FOR FIXED SIDEBARS
alltypes = getAllItemtypes(db.session, Itemtype) #ALWAYS PUT THIS LINE
roles = []
res_all_itemtypes = [] 
	
for each in alltypes :
	roles.append(getItemtypeIDRoles(db.session,Item,Participation,each.item_type_id))

res_all_itemtypes = list(zip(alltypes,roles))
##########################   END FOR SIDEBARS
####### NEVER FORGET TO PUT IN render_template: typeslist = res_all_itemtypes







@app.route('/a')
def AllTypesWithRoles():
	return str(res_all_itemtypes)

@app.route('/')
def home():
	return render_template('pages/home.html', typeslist=res_all_itemtypes)


#######################MODIFS THOMAS#############################
@app.route('/login')
def home_page():
    return render_template("pages/login.html") #TODO

# The Members page is only accessible to authenticated users
@app.route('/members')
@login_required      # Use of @login_required decorator
def members_page():
    return "Ceci est possible que pour ceux qui sont confirmés"
#######################FIN MODIFS THOMAS#############################



@app.route('/All')
def itemlist_All_alphabetic():
	return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items = getAllItems(db.session, Item, Itemtype), filter_requested = "Alphabetic order", displayRoles = 'no')
	
@app.route('/All/<myfilter>')
def itemlist_All_sorted(myfilter):
	if myfilter == 'Roles':
		a = getAllRoles(db.session, Participation)
		b = [ x[0] for x in a ]
		return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items = b, filter_requested = myfilter, displayRoles = 'yes')
	else:
		return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items = getAllItems_WithFilter(db.session,Item,Itemtype, myfilter), filter_requested = myfilter, displayRoles = 'no')

#To display a requested list
@app.route('/<itemtype_name>/<myfilter>')
def itemlist_Types(itemtype_name,myfilter):
	mytypeID = getIdOfItemtype(db.session,Itemtype,itemtype_name)
	
	return render_template('pages/requested_list.html', typeslist=res_all_itemtypes, list_requested = getAllItemsOfThisIDType_WithFilter(db.session,Item,Itemtype, myfilter, mytypeID), filter_requested = myfilter, type_requested = itemtype_name.title())

##THIS IS DONE TWICE (IF URL /ITEMTYPE or /ITEMTYPE/)
#To display a requested list in alphabetic order
@app.route('/<itemtype_name>')
def itemlist_Types_alphabetic(itemtype_name):
	mytypeID = getIdOfItemtype(db.session,Itemtype,itemtype_name)
	
	if mytypeID>0:
		redir = '/'+itemtype_name +'/All'
		return redirect(redir)
	else:
		return redirect('/')
#To display a requested list in alphabetic order
@app.route('/<itemtype_name>/')
def itemlist_Types_alphabeticBIS(itemtype_name):
	redir = '/' + itemtype_name
	return redirect(redir)


#To display a requested list from keywords
@app.route('/search',  methods=['POST'])
def searchByKeywords():
	keyWords = request.form.get('Mysearch')
	mylist = keywordSearch(db.session,Participant,Item,keyWords)
	isAnItem = []
	itemName = []
	temp = ()
	res = ()
	
	#Test if the found object is item: if yes then true
	for each in mylist:
		isAnItem.append(isinstance(each,Item))
	
	temp = list(zip(mylist,isAnItem))
	
	#x: list and y: true (Item) & false (Participant)
	itemName = [db.session.query(Itemtype).filter(Itemtype.item_type_id == x.type_id).one().type_name if y else 'Participant' for (x,y) in temp ]
	
	#(details, item/participant)
	res = list(zip(mylist,itemName))
	
	ParticipantCounter = [db.session.query(Participation).filter(Participation.participant_id == x.participant_id).count() if y =='Participant' else 0 for (x,y) in res ]
	
	#((details, item/participant),nbOfItems)
	final_res = list(zip(res,ParticipantCounter))
	
	#return str(final_res)
	return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested = final_res, type_requested = "Search results",MyKeywords = keyWords)
	
#if the user is trying to reach /search in the url
@app.route('/search')
def search():
	return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested = "", type_requested = "Search results")


#all roles in ALL TYPES
@app.route('/Roles')
def redirToAllRoles():
	return redirect('/All/Roles')

	

#all roles in ONE GIVE NAME OF ITEM TYPE
@app.route('/<mytypeName>/Roles')
def AllRoles_ItemTypeName(mytypeName):
	mytypeID = getIdOfItemtype(db.session, Itemtype, mytypeName)
	
	if mytypeID >0:
		rol = getItemtypeIDRoles(db.session,Item,Participation,mytypeID)
			
	return render_template('pages/roles.html', typeslist=res_all_itemtypes, list_requested = rol, filter_requested = myrole, type_requested = mytypeName, ItsARole = -1)

#list of A GIVEN ROLE of A GIVEN TYPE
@app.route('/<mytypeName>/Roles/<myrole>')
def OneRole_ItemTypeName(mytypeName,myrole):
	mytypeID = getIdOfItemtype(db.session, Itemtype, mytypeName)
	rol = getItemtypeIDRoles(db.session,Item,Participation,mytypeID)
	
	WhoHaveThisRole = getWhoHaveThisRole(db.session, Participant, Participation, myrole)
	#return str(WhoHaveThisRole[0].participant_id)
	return render_template('pages/roles.html', typeslist=res_all_itemtypes, list_requested = WhoHaveThisRole, filter_requested = myrole, type_requested = mytypeName, ItsARole = 0)



#To display one participant
@app.route('/<mytypeName>/Roles/<int:myparticipantID>/<myparticipantName>')
def description_Participant(mytypeName,myparticipantID,myparticipantName):
	return "ok this is for displaying participant"




#To display one item
@app.route('/<itemtype_name>/<int:myitemtypeID>/<myItemName>')
def description_Item(itemtype_name,myitemtypeID,myItemName):
	return "ok this is for displayint item details"


#Handling error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/error.html', typeslist=res_all_itemtypes)

if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run()
