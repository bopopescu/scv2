from sqlalchemy import select,and_,func,Date,cast
from datetime import date,datetime,timedelta



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

def queryAllParticipantsInfo(session,Itemtype,ItemClass,ParticipantClass,ParticipationClass,item):

	return session.query(ParticipantClass,ParticipationClass).\
						filter(and_(
                            Itemtype.item_type_id == item.type_id,
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

