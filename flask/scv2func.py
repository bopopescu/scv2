
from sqlalchemy import Table,select,and_,func
from sqlalchemy.orm import mapper
from datetime import date,datetime,timedelta


# Useful functions for the SCV2 project.

# Define empty Classes that will be mapped to DB tables:

class User(object):
    pass
class Item(object):
    pass
class Itemtype(object):
    pass
class Notation(object):
    pass
class Interest(object):
    pass
class Participant(object):
    pass
class Participation(object):
    pass
class Vote(object):
    pass
class Distinction(object):
    pass
class Event(object):
	pass

# Map ALL the Classes !

def mapAll(context_dic):
	tableNames =[  'user',
	 			   'item',
	 			   'item_type',
	 			   'notation',
	 			   'interest',
	 			   'participant',
	 			   'participation',
	 			   'vote',
	 			   'distinction',
	 			   'event']
	Classes = 	[ 	User,
	 				Item,
	 				Itemtype,
	 				Notation,
	 				Interest,
	 				Participant,
	 				Participation,
	 				Vote,
	 				Distinction,
	 				Event]

	for table,Class in zip(tableNames,Classes):
		mapper(Class,context_dic[table] , confirm_deleted_rows=False)



def importContext(engine, metadata):
	d = {}
	tableNames = [ 'user',
	 			   'item',
	 			   'item_type',
	 			   'notation',
	 			   'interest',
	 			   'participant',
	 			   'participation',
	 			   'vote',
	 			   'distinction',
	 			   'event']
	functions = [ importUser,
	 			  importItem,
	 			  importItem_Type,
	 			  importNotation,
	 			  importInterest,
	 			  importParticipant,
	 			  importParticipation,
	 			  importVote,
	 			  importDistinction,
	 			  importEvent ]

	for name,func in zip(tableNames,functions):
		d[name] = func(engine,metadata)
	return d


def importUser(engine,metadata):
	return Table('user', metadata, autoload=True, autoload_with=engine)

def importItem(engine,metadata):
	return Table('item', metadata, autoload=True, autoload_with=engine)

def importItem_Type(engine,metadata):
	return Table('item_type', metadata, autoload=True, autoload_with=engine)

def importNotation(engine,metadata):
	return Table('notation', metadata, autoload=True, autoload_with=engine)

def importInterest(engine,metadata):
	return Table('interest', metadata, autoload=True, autoload_with=engine)

def importParticipant(engine,metadata):
	return Table('participant', metadata, autoload=True, autoload_with=engine)

def importParticipation(engine,metadata):
	return Table('participation', metadata, autoload=True, autoload_with=engine)

def importVote(engine,metadata):
	return Table('vote', metadata, autoload=True, autoload_with=engine)

def importDistinction(engine,metadata):
	return Table('distinction', metadata, autoload=True, autoload_with=engine)

def importEvent(engine,metadata):
	return Table('event', metadata, autoload=True, autoload_with=engine)


# functions with Tables select,where, ...

def alphaItemSearch(context_dic, connection, letter=None, itemtype=None):
    if letter==None or type==None:
        return "ERROR: Give type and starting letter : needed to build DB queries.\n"

    t = connection.begin()
    try:
        startswith_letter = letter + '%' 
        s = select([context_dic['item'].c.title]).where(and_(
                                                	context_dic['item_type'].c.type_name.like(itemtype),
                                                	context_dic['item'].c.title.like(startswith_letter)
                                             			))

        return connection.execute(s)

        t.commit()
    except:
        t.rollback()
        raise

def getAllParticipants(context_dic, connection, ITEM):

    rq = select([context_dic['participant'].c.firstname,
    			 context_dic['participant'].c.lastname,
    			 context_dic['participation'].c.role]).where(
    			 										and_(
    			 											context_dic['item'].c.title.like(ITEM), 
                                                                        and_(context_dic['participation'].c.item_id == context_dic['item'].c.item_id,
                                                                        	 context_dic['participation'].c.participant_id == context_dic['participant'].c.participant_id)))
    return connection.execute(rq)



# functions with session queries

def alphaSearch(session,ItemClass,TypeClass,letter, itemtype):
	
	#First get the id of the type:
	ourtype = session.query(TypeClass).filter(TypeClass.type_name.like(itemtype)).one()

	letter+='%'

	return session.query(ItemClass).filter(ItemClass.type_id == ourtype.item_type_id).filter(ItemClass.title.like(letter)).all()

def queryAllParticipantsInfo(session,ItemClass,ParticipantClass,ParticipationClass,item):

	return session.query(ParticipantClass,ParticipationClass).\
						filter(ItemClass.title.like(item)).\
						filter(ParticipationClass.item_id == ItemClass.item_id).\
						filter(ParticipationClass.participant_id == ParticipantClass.participant_id).\
						all()


def getRecentItems(session, ItemClass, TypeClass, delta, itemtype):


	ourtype = session.query(TypeClass).filter(TypeClass.type_name.like(itemtype)).one()
	
	return session.query(ItemClass).\
						filter(ItemClass.type_id == ourtype.item_type_id).\
						filter( (func.now() - ItemClass.release_date) < delta ).\
						all()







