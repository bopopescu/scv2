from rqst_func_scv2 import *
from base_model_scv2 import *
from flask import Flask 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()

db.create_all()

print('######################################################\n')
print('>>TEST D\'AJOUT D\'USERS EXISTANTS, & MÉTHODE __repr__()\n')


alfredo = User(firstname='alfredo',
			   lastname='freccino',
			   username='freccifredo',
			   birthdate = date(1978,11,24),
			   mail = 'fredoIlPomodoro@italia.it',
			   password = 'unamozzarella')

dbAdd(db.session,alfredo)

db.session.commit()


for participant in Participant.query.all():
    print(participant)
    
for user in User.query.all():
    print(user)

for item in Item.query.all():
    print(item)

for atype in Itemtype.query.all():
    print(atype.item_type_id)


for notation in Notation.query.all():
    print(notation)


print('######################################################\n')
print('>>TEST RECHERCHE PAR ORDRE ALPHABÉTIQUE:\n')

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
	for itemtype in db.session.query(Itemtype.type_name):
		for item in alphaItemSearch(db.session,Item,Itemtype,letter,itemtype[0]):
			print('-----------')
			print("Un(e)",itemtype[0]," commençant par la lettre",letter,"est:", item.title)
			print("\nCeux qui y ont participé:\n")
			for participant,participation in getAllParticipantsInfo(db.session,Item,Participant,Participation,item):
				print(participant.firstname,participant.lastname,"| leur role:",participation.role)

			print('\n')
			

print('######################################################\n')
print('>>TEST RECHERCHE PAR DATE:\n')

threshold = timedelta(weeks=40*52) # date(year,month,day)
print('Liste des items vieux de 40 ans (=',threshold,')\n')
for itemtype in db.session.query(Itemtype.type_name):
	print('Les ',itemtype[0],':\n')
	for item in getRecentItems(db.session, Item, Itemtype, threshold, itemtype[0]):
		print(item)

print('######################################################\n')
print('>>TEST RECHERCHE PAR MOT-CLÉ:\n')

for keyword in ['ciné','CLUB','amour','AmOuR','rock','archive']:
	for output in keywordItemSearch(db.session,Item,keyword):
		print("Avec le mot-clé",keyword,"on obtient: [",output,']')
	print('\n')

print('######################################################\n')
print('>> TEST MOYENNE')

for item in Item.query.all():
    print(item,'\nSa moyenne:',getArithMean(db.session,Notation,item),'\n')

print('######################################################\n')
print('>> TEST TYPE ID AND NAME')

for atype in Itemtype.query.all():
    print(atype.item_type_id, " - ", atype.type_name)

print('######################################################\n')
print('>> TEST ID OF A GIVEN NAME TYPE')

print(getIdOfItemtype(db.session,Itemtype,"Film"))

print('######################################################\n')
print('>> TEST ALL ITEMS OF A GIVEN ID TYPE')

for items in getAlphabeticItemsOfThisType(db.session,Item, 1) :
	print(items.title, items.type_id)

print('######################################################\n')
print('>> TEST NAME OF A GIVEN ID TYPE')

print(getNameOfID_itemtype(db.session,Itemtype, 1))

print('######################################################\n')
print('>> TEST GET ID OF A GIVEN ID TYPE AND A GIVEN NAME')


print(getItemID(db.session, Item, 1,"babar"))
