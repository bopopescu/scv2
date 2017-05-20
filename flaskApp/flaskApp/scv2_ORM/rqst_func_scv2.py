from sqlalchemy import select,and_,func,Date,cast,exc
from datetime import date,datetime,timedelta
from sqlalchemy.orm.exc import NoResultFound

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


# Retourne un itÃ©rable d'OBJETS:
 ##Â items dont l'attribut title contient "keyword" (NON SENSIBLE Ã€ LA CASSE)

def keywordItemSearch(session,ItemClass,keyword=''):
    keyword = '%'+keyword+'%'
    return session.query(ItemClass).filter(ItemClass.title.ilike(keyword)).all()

# Retourne la moyenne arithmÃ©tique d'un item
 ##Â item EST UN OBJET
  #Â => surcharger si voulu... 

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
 ##Â de STRINGS Ã©tant les roles existant pour cet itemtype donnÃ©
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




from sqlalchemy import select,and_,func,Date,cast,exc,or_
from datetime import date,datetime,timedelta
from functools import reduce

# Session functions:

# functions with session queries:

## This is the main ORM tool to use with SQLAlchemy:
 ## the aim is to store all useful query functions here.



# Retourne un itÃ©rable d'OBJETS:
 ##Â items dont l'attribut title contient "keyword" (NON SENSIBLE Ã€ LA CASSE)

def keywordItemSearch(session,ItemClass,keyword):
    keyword = '%'+keyword+'%'
    return session.query(ItemClass).filter(ItemClass.title.ilike(keyword)).all()

## TolÃ¨re: un keyword sous la forme d'une phrase, ramÃ¨ne tous les Items qui matchent

def keywordC_ItemSearch(session,ItemClass,keyword):

	words = keyword.split(' ')
	L = [ '%'+word+'%' for word in words if word is not '']

	res = [ ItemClass.title.ilike(word) for word in L]

	return session.query(ItemClass).filter(reduce(lambda x,y:or_(x,y) , res)).all()

def keywordC_partSearch(session,ParticipantClass,keyword):

	words = keyword.split(' ')
	L = [ '%'+word+'%' for word in words if word is not '']

	res1 = [ ParticipantClass.firstname.ilike(word) for word in L]
	res2 = [ ParticipantClass.lastname.ilike(word) for word in L]

	final_list = session.query(ParticipantClass).filter(reduce(lambda x,y:or_(x,y) , res1)).all()
	final_list.extend(session.query(ParticipantClass).filter(reduce(lambda x,y:or_(x,y) , res2)).all())

	return final_list

def popKeyWords(session,ParticipationClass,ParticipantClass,newwords,var='descent'):

	if var is 'descent':

		final_list = []

		while not (len(final_list) > 0):
		
			newwords = [ word[:-1] for word in newwords if (word[:-1] is not '' and len(word[:-1])>3)]

			if (len(newwords) ==0):
				break

			newL = [ '%'+word+'%' for word in newwords]

			print("new try:",newL,"\n")
			res = [ ParticipationClass.role.ilike(word) for word in newL]

			for part,_ in session.query(ParticipantClass,ParticipationClass).\
								filter(and_(
									ParticipantClass.participant_id == ParticipationClass.participant_id,
									reduce(lambda x,y:or_(x,y) , res)
									)).\
								all():
				final_list.append(part)


		print("Found! ",newwords,'\n')

		return final_list

	if var is 'ascent':

		final_list = []

		while not (len(final_list) > 0):
		
			newwords = [ word[1:] for word in newwords if word[1:] is not '']

			if (len(newwords) ==0):
				break

			newL = [ '%'+word+'%' for word in newwords]

			print("new try:",newL,"\n")
			res = [ ParticipationClass.role.ilike(word) for word in newL]

			for part,_ in session.query(ParticipantClass,ParticipationClass).\
								filter(and_(
									ParticipantClass.participant_id == ParticipationClass.participant_id,
									reduce(lambda x,y:or_(x,y) , res)
									)).\
								all():
				final_list.append(part)


		print("Found! ",newwords,'\n')

		return final_list






def keywordC_roleSearch(session,ParticipationClass,ParticipantClass,keyword):

	words = keyword.split(' ')
	L = [ '%'+word+'%' for word in words if word is not '']

	# First try...

	res = [ ParticipationClass.role.ilike(word) for word in L]

	final_list = []
	for part,_ in session.query(ParticipantClass,ParticipationClass).\
							filter(and_(
								ParticipantClass.participant_id == ParticipationClass.participant_id,
								reduce(lambda x,y:or_(x,y) , res)
								)).\
							all():
		final_list.append(part)


	if (len(final_list)>0):
		return final_list #enough...

	# if doesn't work? try all combinations of keyword slices ..

	newwords = words

	global_list = []

	while ( len(newwords) > 0):
		newwords = [ word[1:] for word in newwords if word[1:] is not '']
		global_list.extend(popKeyWords(session,ParticipationClass,ParticipantClass,newwords,var='descent'))
		

	return global_list

##Â Fonction FINALE !!! :D

def keywordSearch(session,ParticipationClass,ParticipantClass,ItemClass,keyword):

	L = keywordC_ItemSearch(session,ItemClass,keyword)
	L.extend(keywordC_partSearch(session,ParticipantClass,keyword))
	L.extend(keywordC_roleSearch(session,ParticipationClass,ParticipantClass,keyword))

	seen = set()
	seen_add = seen.add
	
	return [ obj for obj in  L if not (obj in seen or seen_add(obj))]

# def keywordItemSearch(session,ItemClass,keyword)

# Retourne la moyenne arithmÃ©tique d'un item
 ##Â item EST UN OBJET
  #Â => surcharger si voulu... 

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
 ##Â de STRINGS Ã©tant les roles existant pour cet itemtype donnÃ©
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


def getAllNotations(session,UserClass,NotationClass,item):

	return session.query(NotationClass,UserClass).\
						filter(
							and_(
								NotationClass.user_id == UserClass.id,
								NotationClass.item_id == item.item_id)).all()

def getParticipantsOfThisItem(session, Participant, Participation, myitemID):
	return session.query(Participant).join(Participation, Participant.participant_id == Participation.participant_id).filter(Participation.item_id == myitemID).all()


#Get all itemtypes (for fixed borders!)
def getAllItemtypes(session, Itemtype):
	return session.query(Itemtype).all()

#Get all items (alphabetic) with ALL TYPES
def getAllItems(session, Item, Itemtype):
	return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).order_by(Item.title).all()

#Get all items (alphabetic) with ONE GIVEN TYPE mytypeID
def getAllItemsOfThisIDType(session, Item, Itemtype, mytypeID):
	return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).filter(Item.type_id == mytypeID).order_by(Item.title).all()
	

#Order by 'myfilter' with ALL TYPES
def getAllItems_WithFilter(session,Item,Itemtype, myfilter):
	if myfilter == 'Best':
		return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).order_by(Item.mean.desc()).all()
	if myfilter == 'Recent':
		return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).order_by(Item.release_date.desc()).all()
	if myfilter == 'Famous': #gotta change this!!!
		return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).order_by(Item.release_date.desc()).all()
	
#Get all ROLES NAMES of ALL Types	
def getAllRoles(session, Participation):
	return session.query(Participation.role).distinct().all()
	
#Order by 'myfilter' with ONE GIVEN TYPE mytypeID
def getAllItemsOfThisIDType_WithFilter(session,Item,Itemtype, myfilter, mytypeID):
	if myfilter == 'All':
		return getAllItemsOfThisIDType(session,Item,Itemtype,mytypeID)
	if myfilter == 'Best':
		return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).filter(Item.type_id == mytypeID).order_by(Item.mean.desc()).all()
	if myfilter == 'Recent':
		return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).filter(Item.type_id == mytypeID).order_by(Item.release_date.desc()).all()
	if myfilter == 'Famous': #gotta change this!!!
		return session.query(Item.item_id, Item.title, Item.release_date, Item.item_id, Item.mean, Itemtype.type_name, Itemtype.item_type_id).join(Itemtype,Item.type_id == Itemtype.item_type_id).filter(Item.type_id == mytypeID).order_by(Item.release_date.desc()).all()

#Get the ID of a given itemtype_name
def getIdOfItemtype(session,Itemtype,itemtype_name):
	try:
		return session.query(Itemtype).filter(Itemtype.type_name == itemtype_name).one().item_type_id
	except NoResultFound:
		return -1

#Get roles of a given mytypeID
def getItemtypeIDRoles(session,ItemClass,ParticipationClass,mytypeID):
	result = session.query(ParticipationClass,ItemClass).\
						filter(ParticipationClass.item_id == ItemClass.item_id).\
						filter(ItemClass.type_id == mytypeID).\
						order_by(ParticipationClass.role).\
						all()


	L = []
	for part,item in result:
		L.append(part.role)

	seen = set()
	seen_add = seen.add

	return [ p for p in  L if not (p in seen or seen_add(p))]

#Get a list of who have myrole in itemtype
def getWhoHaveThisRole(session, Participant, Participation, myrole):
	return session.query(Participant).join(Participation, Participant.participant_id == Participation.participant_id).filter(Participation.role == myrole).all()



#Useful for the fixed sidebars
def mainheader(session, Item, Itemtype, Participation):
	alltypes = getAllItemtypes(session, Itemtype)  # ALWAYS PUT THIS LINE
	roles = []
	res_all_itemtypes = [] 
		
	for each in alltypes :
		roles.append(getItemtypeIDRoles(session, Item, Participation, each.item_type_id))

	return list(zip(alltypes, roles))
