
from scv2_rqstfunc import *
from scv2_base_model import *
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


yoan = User(firstname='Yoan',
            lastname='boayaso',
            username='boyoan',
            birthdate=date(1999,10,11),
            mail='yoyoanso@yahoo.fr',
            password='123'
            )

truc = User(firstname='truc',
            lastname='bidule',
            username='machin',
            birthdate=date(3001,10,21),
            mail='WOW@WOW.wow',
            password='wowowowowow'
            )

one1 = User(firstname='firstname1',
            lastname='lastname1',
            username='imNUMBA1',
            birthdate=date(1,1,1),
            mail='numba@one.first',
            password='imthafirst'
            )


dbAdd(db.session,one1)
dbAdd(db.session,truc)
dbAdd(db.session,yoan)
dbAdd(db.session,alfredo)

db.session.commit()


for user in User.query.all():
    print(user) #use of __repr__ method :)

for item in Item.query.all():
    print(item)

types = Itemtype.query.all()
for sometype in types:
	print(sometype)

for participant in Participant.query.all():
    print(participant)

for part in Participation.query.all():
    print(part)


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

