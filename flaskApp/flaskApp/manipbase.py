import sqlalchemy
from scv2_initfunc import *
from scv2_rqstfunc import *
from sqlalchemy import create_engine,MetaData
import string
from datetime import datetime,timedelta

scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')


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

