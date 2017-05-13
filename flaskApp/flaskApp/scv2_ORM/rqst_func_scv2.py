from sqlalchemy import select,and_,func,Date,cast,exc
from datetime import date,datetime,timedelta

# Session functions:

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


# Retourne un itérable d'OBJETS:
 ## items dont l'attribut title contient "keyword" (NON SENSIBLE À LA CASSE)

def keywordItemSearch(session,ItemClass,keyword):
    keyword = '%'+keyword+'%'
    return session.query(ItemClass).filter(ItemClass.title.ilike(keyword)).all()

# Retourne la moyenne arithmétique d'un item
 ## item EST UN OBJET
  # => surcharger si voulu... 

def getArithMean(session,NotationClass,item):

    notations = session.query(NotationClass).\
                            filter(and_(
                                NotationClass.item_id == item.item_id,
                                NotationClass.note != None)).\
                            all()

    return sum([notation.note for notation in notations]) / max(1,len(notations))


def notedItems(session,NotationClass,user):
    return session.query(NotationClass).\
                        filter(NotationClass.user_id == user.user_id).all()

# Retourne une liste SANS DOUBLONS:
 ## de STRINGS étant les roles existant pour cet itemtype donné
  ### itemtype EST UN OBJET !
   # => surcharger si voulu..

def getItemtypeRoles(session,ItemClass,ParticipationClass,itemtype):
	result = session.query(ParticipationClass,ItemClass).\
						filter(ParticipationClass.item_id == ItemClass.item_id).\
						filter(ItemClass.type_id == itemtype.item_type_id).\
						order_by(ParticipationClass.role).\
						all()


	L = []
	for part,item in result:
		L.append(part.role)

	seen = set()
	seen_add = seen.add

	return [ p for p in  L if not (p in seen or seen_add(p))]


def getParticipantItems(session,ItemClass,ParticipationClass,participant):
	result = session.query(ParticipationClass,ItemClass).\
						filter(and_(
							ParticipationClass.participant_id == participant.participant_id,
							ParticipationClass.item_id == ItemClass.item_id)).\
						order_by(ItemClass.item_id).\
						all()

	L = []
	for part,item in result:
		L.append(item)

	seen = set()
	seen_add = seen.add

	return [ item for item in  L if not (item in seen or seen_add(item))]

def getIdOfItemtype(session,TypeClass,TypeNameClass):
	return session.query(TypeClass).filter(TypeClass.type_name == TypeNameClass).one().item_type_id

def getNameOfID_itemtype(session,TypeClass,TypeIDClass):
	return session.query(TypeClass).filter(TypeClass.item_type_id == TypeIDClass).one().type_name

	
def getAlphabeticItemsOfThisType(session, Item,ItemTypeId):
	return session.query(Item).filter(Item.type_id == ItemTypeId).order_by(Item.title).all()
	
def getItemID(session, Item, myitemtypeID,myItemName):
	return session.query(Item).filter(and_(Item.type_id == myitemtypeID, Item.title == myItemName)).one().item_id
