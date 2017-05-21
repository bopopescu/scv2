from flask import Flask, jsonify, render_template, request, json, redirect, url_for, render_template_string, jsonify, flash, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

from scv2_ORM.rqst_func_scv2 import *
from scv2_ORM.base_model_scv2 import *


from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required

import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import *
import fnmatch
from click.types import File


# Useful list of class names, see flask_admin

classes = [   User,
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


# input("Press Enter to continue...")

UPLOAD_FOLDER = 'static/images/'
UPLOAD_FOLDER_USER = 'static/user/'
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
app.config['UPLOAD_FOLDER_USER'] = UPLOAD_FOLDER_USER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'

db.init_app(app)
app.app_context().push()
mail = Mail(app)  # Initialize Flask-Mail
db.create_all()
# set flask_admin !

admin = Admin(app, name='inScale', template_mode='bootstrap3')

for someClass in classes:
    admin.add_view(ModelView(someClass, db.session))


db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User


@app.before_request
def before_request():
    g.user = current_user

# @login_manager.user_loader
#     user = db.session.query(User).filter(User.id == u_id).one()
#     g.user = user
#     return user


T = [ truc.name for truc in db.metadata.sorted_tables]  # Table names 

# launch phpmyadmin: systemctl restart httpd

###########################  USEFUL FOR FIXED SIDEBARS
res_all_itemtypes = mainheader(db.session, Item, Itemtype, Participation)
###########################   END FOR SIDEBARS
####### NEVER FORGET TO PUT IN render_template: typeslist = res_all_itemtypes


####################login here#############################

@app.route('/user/<user_id>', strict_slashes=False)
def userPage(user_id):
    myUserObject = db.session.query(User).filter(User.id == user_id).one()
    myfile = '0'
    if not os.path.exists('static/user/' + user_id + '/'):
        image_link = "no"
    else :
        for file in os.listdir('static/user/' + user_id + '/'):
            if fnmatch.fnmatch(file, "*" + "_" + str(myUserObject.id) + "*.*"):
                print ('\n\n\n' + file + '\n\n\n')
                myfile = file
                image_link = "/static/user/" + user_id + "/" + myfile 
                break
        
        if myfile == '0' :
            image_link = "no"
    return render_template('pages/user.html', image_link=image_link, user=myUserObject, typeslist=res_all_itemtypes)

@app.route('/user/<user_id>/add', methods=['GET', 'POST'], strict_slashes=False)
def add_picture_User(user_id):
    myUserObject = db.session.query(User).filter(User.id == user_id).one()
    if request.method == 'POST':
        # check if the post request has the file part
        add = -1
        image_link = "upload_error"
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
            if not os.path.exists(app.config['UPLOAD_FOLDER_USER'] + user_id):
                os.makedirs(app.config['UPLOAD_FOLDER_USER'] + user_id)
            filename = myUserObject.username + "_" + user_id + "." + file.filename.split(".")[1]
            if os.path.isfile(app.config['UPLOAD_FOLDER_USER'] + user_id + "/" + filename):
                add = 2
                os.remove(app.config['UPLOAD_FOLDER_USER'] + user_id + "/" + filename)
                # return redirect(url_for('failure'))
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER_USER'] + user_id, filename))
            add = 1
            # return redirect(url_for('success',fileAdd="yes it has been added??"))
            image_link = "/" + app.config['UPLOAD_FOLDER_USER'] + user_id + "/" + filename 
    return redirect(url_for('userPage', user_id=user_id))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# To display one item
@app.route('/<itemtype_name>/<int:myitemID>/<myItemTitle>', methods=['GET', 'POST'], strict_slashes=False)
def description_Item(itemtype_name, myitemID, myItemTitle):
    myItemObject = db.session.query(Item, Itemtype).join(Itemtype, Item.type_id == Itemtype.item_type_id).filter(Item.item_id == myitemID).one()
    myItemPartcipants = getParticipantsOfThisItem(db.session, Participant, Participation, myitemID)
    myNbReviews = db.session.query(Notation).filter(Notation.item_id == myitemID).count()
    myfile = '0'
    if not os.path.exists('static/images/' + itemtype_name + '/'):
        image_link = "noo"
    else :
        for file in os.listdir('static/images/' + itemtype_name + '/'):
            if fnmatch.fnmatch(file, '*' + myItemTitle + '*.*'):
                print ('\n\n\n' + file + '\n\n\n')
                myfile = file
                image_link = "/static/images/" + itemtype_name + "/" + myfile 
                break
        
        if myfile == '0' :
            image_link = "no"

    add_res = None
    user_note = None

    if request.method == 'POST':

        note = request.form['starvalue']
        i_id = myitemID
        review = request.form['comment']

        q = db.session.query(Notation).filter(db.and_(Notation.item_id == myitemID, Notation.user_id == g.user.id))

        if q.count() == 0:
            u_id = request.form['user_id']
            add_res = dbAdd(db.session, Notation(item_id=i_id, user_id=u_id, note=note, review_link=review))
            db.session.commit()
        else:
            # got to update:
            item_update = q.one()

            item_update.note = note
            item_update.review_link = review
            db.session.commit()
        # On recalcule la moyenne

        current_item = db.session.query(Item).filter(Item.item_id == myitemID).one()

        current_item.mean = getArithMean(db.session, Notation, current_item)

        db.session.commit()

        print("\n\nGOTTEM? \n", request.form.to_dict())


    # On check si user connecté, si data dans DB..

    if g.user.is_active:
        q = db.session.query(Notation).filter(db.and_(Notation.item_id == myitemID, Notation.user_id == g.user.id))

        if q.count() > 0:
            user_note = q.one()
    return render_template('pages/item.html', image_link=image_link, typeslist=res_all_itemtypes, myitem=myItemObject, myparticipants=myItemPartcipants, add_res=add_res, user_note=user_note, myNbReviews=myNbReviews)
         

@app.route('/<itemtype_name>/<int:myitemID>/<myItemTitle>/reviews', methods=['GET', 'POST'], strict_slashes=False)
def allnotes_Item(itemtype_name, myitemID, myItemTitle):

    current_item = db.session.query(Item).filter(Item.item_id == myitemID).one()
    if current_item is not None:
        return render_template('pages/allnotes.html', current_item=current_item, comment_list=getAllNotations(db.session, User, Notation, current_item), typeslist=res_all_itemtypes)
    else:
        return redirect(url_for("page_not_found"))
        
# To display one add picture item
@app.route('/<itemtype_name>/<int:myitemID>/<myItemTitle>/add', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_picture_Item(itemtype_name, myitemID, myItemTitle):
    myItemPartcipants = getParticipantsOfThisItem(db.session, Participant, Participation, myitemID)
    myItemObject = db.session.query(Item, Itemtype).join(Itemtype, Item.type_id == Itemtype.item_type_id).filter(Item.item_id == myitemID).one()
    myItemTitle = myItemObject[0].title.replace(" ", "_")
    myNbReviews = db.session.query(Notation).filter(Notation.item_id == myitemID).count()
    add_res = None
    user_note = None
    if request.method == 'POST':
        # check if the post request has the file part
        add = -1
        image_link = "upload_error"
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
            filename = myItemTitle + "." + file.filename.split(".")[1]
            if os.path.isfile(app.config['UPLOAD_FOLDER'] + itemtype_name + "/" + filename):
                add = 0
                image_link = "/" + app.config['UPLOAD_FOLDER'] + itemtype_name + "/" + filename 
                # return redirect(url_for('failure'))
            else :
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + itemtype_name, filename))
                add = 1
                # return redirect(url_for('success',fileAdd="yes it has been added??"))
                image_link = "/" + app.config['UPLOAD_FOLDER'] + itemtype_name + "/" + filename
            myItemObject[0].image_link = image_link
            db.session.commit()
            return render_template('pages/item.html', add_res=add_res, user_note=user_note, add=add, image_link=image_link, typeslist=res_all_itemtypes, myitem=myItemObject, myparticipants=myItemPartcipants)
    else:
        return redirect('/')

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


@app.route('/All', strict_slashes=False)
def itemlist_All_alphabetic():
	# return str(getAllItems(db.session, Item, Itemtype))
	return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items=getAllItems(db.session, Item, Itemtype), filter_requested="Alphabetic order", displayRoles='no')
	
@app.route('/All/<myfilter>', strict_slashes=False)
def itemlist_All_sorted(myfilter):
	if myfilter == 'Roles':
		a = getAllRoles(db.session, Participation)
		b = [ x[0] for x in a ]
		return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items=b, filter_requested=myfilter, displayRoles='yes')
	else:
		return render_template('pages/all_items.html', typeslist=res_all_itemtypes, all_items=getAllItems_WithFilter(db.session, Notation, Item, Itemtype, myfilter), filter_requested=myfilter, displayRoles='no')

# To display a requested list
@app.route('/<itemtype_name>/<myfilter>', strict_slashes=False)
def itemlist_Types(itemtype_name, myfilter):
	mytypeID = getIdOfItemtype(db.session, Itemtype, itemtype_name)
	return render_template('pages/requested_list.html', typeslist=res_all_itemtypes, list_requested=getAllItemsOfThisIDType_WithFilter(db.session, Item, Itemtype, myfilter, mytypeID), filter_requested=myfilter, type_requested=itemtype_name.title())

# #THIS IS DONE TWICE (IF URL /ITEMTYPE or /ITEMTYPE/)
# To display a requested list in alphabetic order
@app.route('/<itemtype_name>', strict_slashes=False)
def itemlist_Types_alphabetic(itemtype_name):
	mytypeID = getIdOfItemtype(db.session, Itemtype, itemtype_name)
	
	if mytypeID > 0:
		redir = '/' + itemtype_name + '/All'
		return redirect(redir)
	else:
		return redirect('/')

# To display a requested list from keywords
@app.route('/search', methods=['POST'], strict_slashes=False)
def searchByKeywords():
	keyWords = request.form.get('Mysearch')
	
	if keyWords:
		mylist = keywordSearch(db.session, Participation, Participant, Item, keyWords)
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
	else:
		final_res = ""
			
	# return str(mylist)
	# return str(final_res)
	return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested=final_res, type_requested="Search results", MyKeywords=keyWords)
	
# if the user is trying to reach /search in the url

@app.route('/search', methods=['GET'], strict_slashes=False)
def search():
	return render_template('pages/search_results.html', typeslist=res_all_itemtypes, list_requested="", type_requested="Search results")

# all roles in ALL TYPES
@app.route('/Roles', strict_slashes=False)
def redirToAllRoles():
	return redirect('/All/Roles')
	
# get all participants from THIS Role
@app.route('/Roles/<nameofrole>', strict_slashes=False)
def participantsOfThisROle(nameofrole): 
	
	participantsOfTheRole = db.session.query(Participant.participant_id, Participant.firstname, Participant.lastname, Participant.picture_link).distinct(Participant.participant_id, Participation.participant_id).filter(and_(Participation.participant_id == Participant.participant_id, Participation.role == nameofrole)).all()
	thefilter = "Here is the list of the " + nameofrole.lower() + "s you are searching for:"
	res = []
	finalres = []
	
	for each in participantsOfTheRole:
		res = (each.participant_id, each.firstname, each.lastname, each.picture_link, db.session.query(Itemtype.type_name, Participation.item_id, Item.title).distinct(Participation.participant_id).filter(Participation.participant_id == each.participant_id, Participation.item_id == Item.item_id, Item.type_id == Itemtype.item_type_id, Participation.role == nameofrole).all())
		finalres.append(res)
	
	# finalres structure: [participant_id, firstname, lastname, picture_link, object]
	# and object = [ (typename1, item_id1, title1), (typename2, item_id2, title2), (typename3, item_id3, title3), ... ]
	
	# return str(finalres)
	return render_template('pages/requested_list.html', typeslist=res_all_itemtypes, list_requested=finalres, filter_requested=thefilter, type_requested=nameofrole)


# To display one participant
@app.route('/Roles/<int:myparticipantID>/<myparticipantName>', strict_slashes=False)
def description_Participant(myparticipantID, myparticipantName):
	myparticipantDetails = db.session.query(Participant).filter(Participant.participant_id == myparticipantID).one()
	myitemsObject = db.session.query(Participation.role, Item.item_id, Item.title, Itemtype.type_name, Item.mean).filter(Participation.item_id == Item.item_id, Item.type_id == Itemtype.item_type_id, Participation.participant_id == myparticipantID).all()
	myrolesObject = db.session.query(Participation.role).distinct(Participation.role).filter(Participation.participant_id == myparticipantID).all()
	res = []
	finalres = []
	
	for eachitem in myitemsObject:
		oldres = res
		res = (eachitem.role, db.session.query(Item.item_id, Item.title, Item.release_date, Item.mean, Itemtype.type_name).filter(Participation.item_id == Item.item_id, Participation.role == eachitem.role, Participation.participant_id == myparticipantID, Itemtype.item_type_id == Item.type_id).all())
		if (oldres != res):
			finalres.append(res)
	
	# finalres : [ (role1, (item1 where im role1, item2 where im role1 ,...)), (role2, (item1 where im role2, item2 where im role2 ,...))]
	# return str(finalres)
	return render_template('pages/onerole.html', typeslist=res_all_itemtypes, mydetails=myparticipantDetails, myitems=finalres, myroles=myrolesObject)
    

	

# all roles in ONE GIVE NAME OF ITEM TYPE
@app.route('/<mytypeName>/Roles', strict_slashes=False)
def AllRoles_ItemTypeName(mytypeName):
	mytypeID = getIdOfItemtype(db.session, Itemtype, mytypeName)
	
	if mytypeID > 0:
		rol = getItemtypeIDRoles(db.session, Item, Participation, mytypeID)
	else:
		return redirect(url_for("page_not_found"))
			
	return render_template('pages/roles.html', typeslist=res_all_itemtypes, list_requested=rol, filter_requested=myrole, type_requested=mytypeName, ItsARole=-1)

# list of A GIVEN ROLE of A GIVEN TYPE
@app.route('/<mytypeName>/Roles/<myrole>', strict_slashes=False)
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

@app.errorhandler(403)
def page_not_found(e):
    return render_template('pages/error.html', typeslist=res_all_itemtypes)

@app.errorhandler(400)
def page_not_found(e):
    return render_template('pages/error.html', typeslist=res_all_itemtypes)


if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.debug = True
    app.run(port=5000)
