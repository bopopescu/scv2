import sqlalchemy
from sqlalchemy.orm import sessionmaker
from scv2_initfunc import *
from scv2_rqstfunc import *
from sqlalchemy import create_engine,MetaData
import string
from datetime import datetime,timedelta

scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')

metadata = MetaData(scv2_engine)

tables = importContext(scv2_engine,metadata)

#OK BOYS ! GO SESSION, MAPPING, INFINITE POOOOWERRR !!! 

Session = sessionmaker(bind=scv2_engine) # Session class

session = Session() # object constructor

mapAll(tables)

#has this worked ?

print ('=====================================================')
print ('|	      Trying out the session !	  	    |')
print ('=====================================================\n\n')


print('######################################################\n')
print('>>TEST D\'AJOUT D\'USERS EXISTANTS, & MÉTHODE __repr__()\n')

alfredo = User()
alfredo.firstname='alfredo'
alfredo.lastname='freccino'
alfredo.username='freccifredo'
alfredo.birthdate = date(1978,11,24)
alfredo.mail = 'fredoIlPomodoro@italia.it'
alfredo.password = 'unamozzarella'

yoan = User(firstname='Yoan',
			lastname='boayaso',
			username='boyoan',
			birthdate=date(1999,10,11),
			mail='yoyoanso@yahoo.fr'
			)
yoan.password='abc123'



safeAdd(session,yoan)
safeAdd(session,alfredo)

session.commit()


for user in session.query(User):
	print(user) #use of __repr__ method :) 


#FIN DES SUPPRESSIONS DE DOUBLONS !

session.flush()
session.commit()



print('######################################################\n')
print('>>TEST RECHERCHE PAR ORDRE ALPHABÉTIQUE:\n')

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
	for itemtype in session.query(Itemtype.type_name):
		for item in alphaItemSearch(session,Item,Itemtype,letter,itemtype[0]):
			print('-----------')
			print("Un(e)",itemtype[0]," commençant par la lettre",letter,"est:", item.title)
			print("\nCeux qui y ont participé:\n")
			for participant,participation in getAllParticipantsInfo(session,Item,Participant,Participation,item):
				print(participant.firstname,participant.lastname,"| leur role:",participation.role)

			print('\n')

print('######################################################\n')
print('>>TEST RECHERCHE PAR DATE:\n')

threshold = timedelta(weeks=40*52) # date(year,month,day)
print('Liste des items vieux de 40 ans (=',threshold,')\n')
for itemtype in session.query(Itemtype.type_name):
	print('Les ',itemtype[0],':\n')
	for item in getRecentItems(session, Item, Itemtype, threshold, itemtype[0]):
		print(item)

print('######################################################\n')
print('>>TEST RECHERCHE PAR MOT-CLÉ:\n')

for keyword in ['ciné','CLUB','amour','AmOuR','rock','archive']:
	for output in keywordItemSearch(session,Item,keyword):
		print("Avec le mot-clé",keyword,"on obtient: [",output,']')
	print('\n')
# REQUETES AVEC SELECT TOUJOURS DISPONIBLES ! 

# print ("<><><><><><><> Requêtes et companie ;) <><><><><><><>\n")

# item_type = tables['item_type']
# item = tables['item']
# item_type = tables['item_type']
# notation = tables['notation']
# interest = tables['interest']
# participant = tables['participant']
# participation = tables['participation']
# vote = tables['vote']
# distinction = tables['distinction']
# event = tables['event']

# conn = scv2_engine.connect()

# for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':

#     WOW = alphaItemSearch(tables,conn,letter,'Film')

#     for wows in WOW:
#         print("Films de la base de donnée commençant par ",letter," : ",wows)



# s = select([item.c.title])

# for titles in conn.execute(s):
#     print('------------------')
#     print(titles[0])
#     print('------------------')
#     for data in getAllParticipants(tables,conn,titles[0]):
#         print(data)


# conn.close()




############################
#PARTIE JADY AVEC SELECT   #
############################


print("\n\n")
print("---------------CECI EST POUR LA RECHERCHE PAR MOT-CLE---------------\n")


c = scv2_engine.connect()

print("-----Connexion OK-----")

print("-----ALL ITEMS-----")
for item in getAllItems(c):
	print(item.title, "(id: ", item.item_id, ", type_id: ", item.type_id,")")
	print("releasing date: ",item.release_date)
	print("\n")
	
	
keyword = "Imaginaire"
print("-----ONLY",keyword,"-----")

for item in getItemWithKeyWord(c,keyword):
	print("id: ", item.item_id, ", type_id: ", item.type_id)
	print(item.title)
	print("releasing date: ",item.release_date)
	print("typename: ",item.type_name)
	print("\n")
	

print("\n\n")
print("---------------CECI EST POUR LA RECHERCHE DES PARTICIPANTS-------------\n")
for rqst in getIdOfThisItem(c,"babar"):
	print("-----item id:",rqst.item_id,"----")
	for item in getParticipantsOfThisItem(c,rqst.item_id):
		print(item.title)
		print(item.participant_id ,":",item.firstname, item.lastname)
		print(item.birthdate)
		print("\n")


c.close()

print("-------------FIN RECHERCHES------------")

print("\n\n")
print("---------------CECI EST POUR LA RECHERCHE PAR MOT-CLE---------------\n")


c = scv2_engine.connect()

print("-----Connexion OK-----")

print("-----ALL ITEMS-----")
for item in getAllItems(c):
	print(item.title, "(id: ", item.item_id, ", type_id: ", item.type_id,")")
	print("releasing date: ",item.release_date)
	print("\n")
	
	
keyword = "Imaginaire"
print("-----ONLY",keyword,"-----")

for item in getItemWithKeyWord(c,keyword):
	print("id: ", item.item_id, ", type_id: ", item.type_id)
	print(item.title)
	print("releasing date: ",item.release_date)
	print("typename: ",item.type_name)
	print("\n")
	

print("\n\n")
print("---------------CECI EST POUR LA RECHERCHE DES PARTICIPANTS-------------\n")
for rqst in getIdOfThisItem(c,"babar"):
	print("-----item id:",rqst.item_id,"----")
	for item in getParticipantsOfThisItem(c,rqst.item_id):
		print(item.title)
		print(item.participant_id ,":",item.firstname, item.lastname)
		print(item.birthdate)
		print("\n")


c.close()

print("-------------FIN RECHERCHES------------")

