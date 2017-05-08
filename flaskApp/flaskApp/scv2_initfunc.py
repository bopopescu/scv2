
from sqlalchemy import Table,select,and_,func,Date,cast
from sqlalchemy.orm import mapper
from datetime import date,datetime,timedelta


# Useful functions for the SCV2 project.

# Define empty Classes that will be mapped to DB tables:

class User(object):
    def __init__(self, firstname=None,lastname=None,username=None,birthdate=None,mail=None, password=None,picture_link=None,bio_link=None):
    	self.firstname=firstname
    	self.lastname=lastname
    	self.username=username
    	self.birthdate=birthdate
    	self.mail=mail
    	self.password=password
    	self.picture_link=picture_link
    	self.bio_link=bio_link

    def __repr__(self):
    	return 'name: '+self.firstname+' '+self.lastname+'| username: '+self.username

class Item(object):
	def __init__(self, title=None,release_date=None,type_id=None,image_link=None,video_link=None,desc_link=None,mean=None):
		self.title=title
		self.release_date=release_date
		self.type_id=type_id
		self.image_link=image_link
		self.video_link=video_link
		self.desc_link=desc_link
		self.mean=mean

	def __repr__(self):
		return 'title: '+self.title+'| date: '+str(self.release_date)+'| id: '+self.type_id.__repr__()



class Itemtype(object):
	def __init__(self,type_name=None):
		self.type_name=type_name
	def __repr__(self):
		return 'id: '+self.item_type_id.__repr__()+'| name: '+self.type_name
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








