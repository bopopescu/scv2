from flask import Flask, jsonify, render_template, request, json, redirect, url_for, render_template_string, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

from scv2_ORM.rqst_func_scv2 import *
from scv2_ORM.base_model_scv2 import *

from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import *
import fnmatch

# Useful list of class names, see flask_admin

classes =   [   User,
                Item,
                Itemtype,
                Notation,
                InterestItem,
                InterestTag,
                Participant,
                Participation,
                Vote,
                Distinction,
                Event]


#input("Press Enter to continue...")

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


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
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"Inscale" <gros.brother@gmail.com>')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

    # Flask-User settings
    USER_APP_NAME = "Inscale"  # Used by email templates
    

app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config.from_object(__name__ + '.ConfigClass')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()
mail = Mail(app)  # Initialize Flask-Mail
db.create_all()
#set flask_admin !

admin = Admin(app, name='inScale', template_mode='bootstrap3')

for someClass in classes:
    admin.add_view(ModelView(someClass, db.session))


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
@app.route('/<itemtype_name>/<int:myitemID>/<myItemTitle>',methods=['GET','POST'])
def description_Item(itemtype_name, myitemID, myItemTitle):
    myItemObject = db.session.query(Item, Itemtype).join(Itemtype, Item.type_id == Itemtype.item_type_id).filter(Item.item_id == myitemID).one()
    myItemPartcipants = getParticipantsOfThisItem(db.session, Participant, Participation, myitemID)
    myfile = '0'
    myItemTitle = myItemObject[0].title.replace(" ","_")
    from click.types import File
    if not os.path.exists('static/images/'+itemtype_name+'/'):
        image_link = "noo"
    else :
        for file in os.listdir('static/images/'+itemtype_name+'/'):
            if fnmatch.fnmatch(file, '*'+myItemTitle+'*.*'):
                print ('\n\n\n'+file+'\n\n\n')
                myfile=file
                image_link="/static/images/"+itemtype_name+"/"+myfile 
                break
        
        if myfile=='0' :
            image_link="no"

    add_res = None

    if request.method == 'POST':

        note = request.form['starvalue']
        i_id = myitemID
        review = request.form['comment']

        u_id = request.form['user_id']
        add_res = dbAdd(db.session,Notation(item_id=i_id,user_id=u_id,note=note,review_link=review))

        print("\n\nGOTTEM? \n",request.form.to_dict())

    return render_template('pages/item.html',image_link=image_link, typeslist=res_all_itemtypes, myitem=myItemObject, myparticipants=myItemPartcipants,add_res=add_res)
         

# To display one add picture item

@app.route('/<itemtype_name>/<int:myitemID>/<myItemTitle>/add', methods=['GET', 'POST'])
def add_picture_Item(itemtype_name, myitemID, myItemTitle):
    myItemPartcipants = getParticipantsOfThisItem(db.session, Participant, Participation, myitemID)
    myItemObject = db.session.query(Item, Itemtype).join(Itemtype, Item.type_id == Itemtype.item_type_id).filter(Item.item_id == myitemID).one()
    myItemTitle = myItemObject[0].title.replace(" ","_")

    if request.method == 'POST':
        # check if the post request has the file part
        add = -1
        image_link="upload_error"
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
            filename = secure_filename(file.filename)
            # filename="cool"+file.filename.rsplit('.', 1)[1].lower()
            if not os.path.exists(app.config['UPLOAD_FOLDER'] + itemtype_name):
                os.makedirs(app.config['UPLOAD_FOLDER'] + itemtype_name)
            filename = myItemTitle+ "." + file.filename.split(".")[1]
            if os.path.isfile(app.config['UPLOAD_FOLDER'] +itemtype_name+"/"+ filename):
                add = 0
                image_link="/"+app.config['UPLOAD_FOLDER']+itemtype_name+"/"+filename 
                #return redirect(url_for('failure'))
            else :
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+itemtype_name, filename))
                add=1
                #return redirect(url_for('success',fileAdd="yes it has been added??"))
                image_link="/"+app.config['UPLOAD_FOLDER']+itemtype_name+"/"+filename 
    return render_template('pages/item.html',add=add, image_link=image_link, typeslist=res_all_itemtypes, myitem=myItemObject, myparticipants=myItemPartcipants)


@app.route('/a')
def AllTypesWithRoles():
	return str(res_all_itemtypes)

@app.route('/')
def home():
	return render_template('pages/home.html', typeslist=res_all_itemtypes)


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
    if keyWords is None:
        keyWords = ''

    mylist = keywordSearch(db.session,Participation,Participant,Item,keyWords)
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
	
	#return str(mylist)
	#return str(final_res)
    return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested=final_res, type_requested="Search results", MyKeywords=keyWords)
	
# if the user is trying to reach /search in the url

@app.route('/search', methods=['GET'])
def search():
	return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested="", type_requested="Search results")

# all roles in ALL TYPES
@app.route('/Roles')
def redirToAllRoles():
	return redirect('/All/Roles')


# To display one participant
@app.route('/Roles/<int:myparticipantID>/<myparticipantName>')
def description_Participant(myparticipantID, myparticipantName):
	return "ok this is for displaying participant"


	

# all roles in ONE GIVE NAME OF ITEM TYPE
@app.route('/<mytypeName>/Roles')
def AllRoles_ItemTypeName(mytypeName):
	mytypeID = getIdOfItemtype(db.session, Itemtype, mytypeName)
	
	if mytypeID > 0:
		rol = getItemtypeIDRoles(db.session, Item, Participation, mytypeID)
	else:
		return redirect(url_for("page_not_found"))
			
	return render_template('pages/roles.html', typeslist=res_all_itemtypes, list_requested=rol, filter_requested=myrole, type_requested=mytypeName, ItsARole=-1)

# list of A GIVEN ROLE of A GIVEN TYPE
@app.route('/<mytypeName>/Roles/<myrole>')
def OneRole_ItemTypeName(mytypeName, myrole):
	mytypeID = getIdOfItemtype(db.session, Itemtype, mytypeName)
	rol = getItemtypeIDRoles(db.session, Item, Participation, mytypeID)
	
	WhoHaveThisRole = getWhoHaveThisRole(db.session, Participant, Participation, myrole)
	# return str(WhoHaveThisRole[0].participant_id)
	return render_template('pages/roles.html', typeslist=res_all_itemtypes, list_requested=WhoHaveThisRole, filter_requested=myrole, type_requested=mytypeName, ItsARole=0)



# Handling error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/error.html', typeslist=res_all_itemtypes)

# Handling error
@app.errorhandler(403)
def page_not_found(e):
    return render_template('pages/error.html', typeslist=res_all_itemtypes)

# Handling error
@app.errorhandler(400)
def page_not_found(e):
    return render_template('pages/error.html', typeslist=res_all_itemtypes)



if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run(port=5000)
