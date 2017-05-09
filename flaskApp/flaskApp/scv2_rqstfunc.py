from sqlalchemy import select,and_,func,Date,cast,exc
from datetime import date,datetime,timedelta

# Session functions:

## Useful safe versions to handle IntegrityErrors from MySQL
 ## In case we concurrently add two times a similar User/Item/Participant/etc...
  ## more "session-oriented" functions to come..

def safeAdd(session,an_object):
    try:
        with session.begin_nested():
            session.add(an_object)
            session.flush()

    except exc.IntegrityError:
        print('Integrity Error, add canceled.\n')
        session.rollback()


# Query functions using SELECT (no SQLA ORM):

## Quite uncommon / outdated, but still functional
 ## example commented in manipbase.py , just in case.

 ## GO BELOW TO SEE THE ORM session.query FUNCTIONS !! 

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



# functions with session queries:

## This is the main ORM tool to use with SQLAlchemy:
 ## the aim is to store all useful query functions here.

def alphaItemSearch(session,ItemClass,TypeClass,letter, itemtype):
	
	#First get the id of the type:
	ourtype = session.query(TypeClass).filter(TypeClass.type_name.like(itemtype)).one()

	letter+='%'

	return session.query(ItemClass).filter(ItemClass.type_id == ourtype.item_type_id).filter(ItemClass.title.like(letter)).all()

def getAllParticipantsInfo(session,ItemClass,ParticipantClass,ParticipationClass,item):

	return session.query(ParticipantClass,ParticipationClass).\
						filter(and_(
                            ItemClass.type_id == item.type_id,
                            and_(
    							ItemClass.title == item.title,
    							and_(
    								ParticipationClass.item_id == ItemClass.item_id),
    								ParticipationClass.participant_id == ParticipantClass.participant_id)
    								)).\
						all()


def getRecentItems(session, ItemClass, TypeClass, timedelta, itemtype):


	ourtype = session.query(TypeClass).filter(TypeClass.type_name.like(itemtype)).one()
	
	return session.query(ItemClass).\
						filter(and_(
							ItemClass.type_id == ourtype.item_type_id),
							ItemClass.release_date < (datetime.utcnow() - timedelta)
							).\
						all()


def keywordItemSearch(session,ItemClass,keyword):
    keyword = '%'+keyword+'%'
    return session.query(ItemClass).filter(ItemClass.title.ilike(keyword)).all()
    
    
############################
#  PARTIE JADY AVEC SELECT #
############################

def getAllItems(connection):
	return connection.execute("SELECT * FROM item;")
	
def getItemWithKeyWord(connection, Keyword, ItemTypeId=None):

	
	if ItemTypeId==None:
		sql  = "SELECT distinct * FROM item, item_type WHERE type_id = item_type_id AND item.title LIKE '%"+ Keyword +"%';"
		
	else:
		sql  = "SELECT distinct * FROM item, item_type WHERE item.title LIKE '%" + Keyword + "%' AND type_id = item_type_id AND type_id = "+str(ItemTypeId)+";"
	
	#print(sql)
	return connection.execute(sql)

def getIdOfThisItem(connection,ItemName=None,ItemTypeId=None):
	if ItemTypeId == None and ItemName == None:
		sql = "select item_id from item;"
		print("search ALL the ids")
	else:
		if ItemTypeId == None:
			sql = "SELECT item_id from item where title LIKE '%" + ItemName + "%';"
		else:
			sql = "SELECT item_id from item where title LIKE '%" + ItemName + "%' and type_id = " + str(ItemTypeID)+";"
	
	
	#print(sql)
	return connection.execute(sql)

def getParticipantsOfThisItem(connection, ItemId):
	
	sql = "SELECT distinct * FROM item, participation, item_type, participant WHERE item.type_id = item_type.item_type_id and participation.item_id = item.item_id and participation.participant_id =  participant.participant_id and  item.item_id = " + str(ItemId)
	#print(sql)
	return connection.execute(sql)

def getAllItems(connection):
	return connection.execute("SELECT * FROM item;")
	
def getItemWithKeyWord(connection, Keyword, ItemTypeId=None):

	
	if ItemTypeId==None:
		sql  = "SELECT distinct * FROM item, item_type WHERE type_id = item_type_id AND item.title LIKE '%"+ Keyword +"%';"
		
	else:
		sql  = "SELECT distinct * FROM item, item_type WHERE item.title LIKE '%" + Keyword + "%' AND type_id = item_type_id AND type_id = "+str(ItemTypeId)+";"
	
	#print(sql)
	return connection.execute(sql)

def getIdOfThisItem(connection,ItemName=None,ItemTypeId=None):
	if ItemTypeId == None and ItemName == None:
		sql = "select item_id from item;"
		print("search ALL the ids")
	else:
		if ItemTypeId == None:
			sql = "SELECT item_id from item where title LIKE '%" + ItemName + "%';"
		else:
			sql = "SELECT item_id from item where title LIKE '%" + ItemName + "%' and type_id = " + str(ItemTypeID)+";"
	
	
	#print(sql)
	return connection.execute(sql)

def getParticipantsOfThisItem(connection, ItemId):
	
	sql = "SELECT distinct * FROM item, participation, item_type, participant WHERE item.type_id = item_type.item_type_id and participation.item_id = item.item_id and participation.participant_id =  participant.participant_id and  item.item_id = " + str(ItemId)
	#print(sql)
	return connection.execute(sql)

def getAllItems(connection):
	return connection.execute("SELECT * FROM item;")
	
def getItemWithKeyWord(connection, Keyword, ItemTypeId=None):

	
	if ItemTypeId==None:
		sql  = "SELECT distinct * FROM item, item_type WHERE type_id = item_type_id AND item.title LIKE '%"+ Keyword +"%';"
		
	else:
		sql  = "SELECT distinct * FROM item, item_type WHERE item.title LIKE '%" + Keyword + "%' AND type_id = item_type_id AND type_id = "+str(ItemTypeId)+";"
	
	#print(sql)
	return connection.execute(sql)

def getIdOfThisItem(connection,ItemName=None,ItemTypeId=None):
	if ItemTypeId == None and ItemName == None:
		sql = "select item_id from item;"
		print("search ALL the ids")
	else:
		if ItemTypeId == None:
			sql = "SELECT item_id from item where title LIKE '%" + ItemName + "%';"
		else:
			sql = "SELECT item_id from item where title LIKE '%" + ItemName + "%' and type_id = " + str(ItemTypeID)+";"
	
	
	#print(sql)
	return connection.execute(sql)

def getParticipantsOfThisItem(connection, ItemId):
	
	sql = "SELECT distinct * FROM item, participation, item_type, participant WHERE item.type_id = item_type.item_type_id and participation.item_id = item.item_id and participation.participant_id =  participant.participant_id and  item.item_id = " + str(ItemId)
	#print(sql)
	return connection.execute(sql)
