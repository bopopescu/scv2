from rqst_func_scv2 import *
from base_model_scv2 import *
from flask import Flask 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()

db.create_all()
"""
for itemtype in Itemtype.query.all():
	print(itemtype)
	print('===================\n')
	print( getItemtypeRoles(db.session,Item,Participation,itemtype) )
	print('\n')


for part in Participant.query.all():
	print(part)
	print('===================\n')
	for item in getParticipantItems(db.session,Item,Participation,part):
		print(item)
	print('\n')


for participant in Participant.query.all():
    print(participant)
    
for user in User.query.all():
    print(user)

for item in Item.query.all():
    print(item)

for atype in Itemtype.query.all():
    print(atype)


for notation in Notation.query.all():
    print(notation)

for truc in keywordC_roleSearch(db.session,Participation,Item,"ill act"):

	print(truc)

"""

keyword = " guillustror "
for truc in keywordSearch(db.session,Participation,Participant,Item,keyword):
	print(truc)