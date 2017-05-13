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
"""

for part in Participant.query.all():
	print(part)
	print('===================\n')
	for item in getParticipantItems(db.session,Item,Participation,part):
		print(item)
	print('\n')

		