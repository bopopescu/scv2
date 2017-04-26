from sqlalchemy import *
from scv2func import *
import string

scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')

metadata = MetaData(scv2_engine)

tables = importContext(scv2_engine,metadata)

item_type = tables['item_type']
item = tables['item']
item_type = tables['item_type']
notation = tables['notation']
interest = tables['interest']
participant = tables['participant']
participation = tables['participation']
vote = tables['vote']
distinction = tables['distinction']
event = tables['event']


print ("<><><><><><><> Requêtes et companie ;) <><><><><><><>\n")

conn = scv2_engine.connect()

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':

    WOW = alphaItemSearch(tables,conn,letter,'Film')

    for wows in WOW:
        print("Films de la base de donnée commençant par ",letter," : ",wows)



s = select([item.c.title])

for titles in conn.execute(s):
    print('-----------------')
    print(titles[0])
    print('-----------------')
    for data in getAllParticipants(tables,conn,titles[0]):
        print(data)


conn.close()
