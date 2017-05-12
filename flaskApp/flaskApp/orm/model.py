from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from sqlalchemy import select, and_, func, Date, cast, exc
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

def dbAdd(session, an_object):
    try:
        session.add(an_object)
        session.flush()

    except exc.IntegrityError:
        print('Integrity Error, add canceled.\n')
        session.rollback()

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    birthdate = db.Column(db.DateTime)
    picture_link = db.Column(db.String(100))
    bio_link = db.Column(db.String(100))
    
    def __init__(self, id=None, active=None, comfirmed_at=None, first_name=None, last_name=None, username=None, birthdate=None, email=None, password=None, picture_link=None, bio_link=None):
        self.first_name = first_name
        self.id = id
        self.last_name = last_name
        self.username = username
        self.active = active
        self.birthdate = birthdate
        self.email = email
        self.password = password
        self.picture_link = picture_link
        self.bio_link = bio_link
        self.comfirmed_at = comfirmed_at
    
    def __repr__(self):
        return 'name: ' + self.first_name + ' ' + self.last_name + '| username: ' + self.username

class Item(db.Model):
    __tablename__ = 'item'
    item_id= db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(35), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    type_id = db.Column( db.Integer, db.ForeignKey("item_type.item_type_id"), nullable=False)
    image_link = db.Column(db.String(100), primary_key=True, nullable=False)
    video_link = db.Column(db.String(100), nullable=False)
    desc_link = db.Column( db.String(100), nullable=False)
    mean = db.Column( db.Float)
    __table_args__ = tuple(db.UniqueConstraint('title','type_id'))

    def __init__(self, title=None,release_date=None,type_id=None,image_link=None,video_link=None,desc_link=None,mean=None):
        self.title=title
        self.release_date=release_date
        self.type_id=type_id
        self.image_link=image_link
        self.video_link=video_link
        self.desc_link=desc_link
        self.mean=mean

    def __repr__(self):
        return 'title: '+self.title+' >> date: '+str(self.release_date)+'| type_id: '+self.type_id.__repr__()

class Itemtype(db.Model):
    __tablename__ = 'item_type'
    item_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, type_name=None):
        self.type_name = type_name
    def __repr__(self):
        return 'id: ' + self.item_type_id.__repr__() + ' >> type_name: ' + self.type_nam

class Notation(db.Model):
    __tablename__ = 'notation'
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    note = db.Column(db.Float, nullable=False)
    review_link = db.Column(db.String(100))
    review_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    upvotes = db.Column(db.Integer)

    def __init__(self, item_id=None, user_id=None, note=None, review_link=None, review_date=None, upvotes=None):
        self.item_id = item_id
        self.user_id = user_id
        self.note = note
        self.review_link = review_link
        self.review_date = review_date
        self.upvotes = upvotes

    def __repr__(self):
        return 'note id: ' + self.note_id.__repr__() + ' >> de user_id: ' + self.user_id.__repr__() + ' pour item_id: ' + self.item_id.__repr__() + ' note: ' + self.note.__repr__()

class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"), nullable=False)
    tagname = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, item_id=None, tagname=None):
        self.item_id = item_id
        self.tagname = tagname

    def __repr__(self):
        return 'id: ' + self.tag_id.__repr__() + ' >> tagname: ' + self.tagname

class InterestTag(db.Model):
    __tablename__ = 'interestTag'
    interest_t_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.tag_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, tag_id=None, user_id=None):
        self.tag_id = tag_id
        self.user_id = user_id

    def __repr__(self):
        return 'id: ' + self.interest_t_id.__repr__() + ' >> user : ' + self.user_id;__repr__() + 'is interested by: ' + self.tag_id.__repr__()

class InterestItem(db.Model):
    __tablename__ = 'interestItem'
    interest_i_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, item_id=None, user_id=None):
        self.item_id = item_id
        self.user_id = user_id

    def __repr__(self):
        return 'id: ' + self.interest_i_id.__repr__() + ' >> user : ' + self.user_id.__repr__() + 'is interested by: ' + self.item_id.__repr__()

class Vote(db.Model):
    __tablename__ = 'vote'
    vote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey("notation.note_id"), nullable=False)
    good = db.Column(db.Boolean)

    __table_args__ = tuple(db.UniqueConstraint('user_id', 'note_id'))

    def __init__(self, user_id=None, note_id=None, good=None):
        self.user_id = user_id
        self.note_id = note_id
        self.good = good

    def __repr__(self):
        return 'id: ' + self.vote_id.__repr__() + ' >> user: ' + self.user_id.__repr__() + ' voted: ' + self.note_id.__repr__() + ' value: ' + self.good.__repr__()

class Participant(db.Model):
    __tablename__ = 'participant'
    participant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20))
    birthdate = db.Column(db.Date, nullable=False, unique=True)
    deathdate = db.Column(db.Date)
    picture_link = db.Column(db.String(100), nullable=False)
    bio_link = db.Column(db.String(100), nullable=False)

    __table_args__ = tuple(db.UniqueConstraint('firstname', 'lastname', 'birthdate'))

    def __init__(self, firstname=None, lastname=None, birthdate=None, deathdate=None, picture_link=None, bio_link=None):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.deathdate = deathdate
        self.picture_link = picture_link
        self.bio_link = bio_link

    def __repr__(self):
        return 'id: ' + self.participant_id.__repr__() + ' >> name: ' + self.firstname + self.lastname + ' born: ' + str(self.birthdate)

class Participation(db.Model):
    __tablename__ = 'participation'
    participation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participant.participant_id"))
    role = db.Column(db.String(50), nullable=False)

    __table_args__ = tuple(db.UniqueConstraint('item_id', 'participant_id', 'role'))

    def __init__(self, item_id=None, participant_id=None, role=None):
        self.item_id = item_id
        self.participant_id = participant_id
        self.role = role

    def __repr__(self):
        return 'id: ' + self.participation_id.__repr__() + ' >> participant: ' + self.participant_id.__repr__() + ' role: ' + self.role

class Distinction(db.Model):
    __tablename__ = 'distinction'
    distinction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participation_id = db.Column(db.Integer, db.ForeignKey("participation.participation_id")),
    event_id = db.Column(db.Integer, db.ForeignKey("event.event_id"))
    award = db.Column(db.String(30), nullable=False)

    __table_args__ = tuple(db.UniqueConstraint('event_id', 'participation_id'))

    def __init__(self, participation_id=None, event_id=None, award=None):
        self.participation_id = participation_id
        self.event_id = event_id
        self.award = award

    def __repr__(self):
        return 'id: ' + self.distinction_id.__repr__() + ' >> award: ' + self.award + ' pour: ' + self.participation_id.__repr__() + ' reçu à: ' + self.event_id.__repr__()

class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_date = db.Column(db.DateTime, nullable=False)
    event_name = db.Column(db.String(20), nullable=False)
    __table_args__ = tuple(db.UniqueConstraint('event_date', 'event_name'))

    def __init__(self, event_date=None, event_name=None):
        self.event_date = event_date
        self.event_name = event_name

    def __repr__(self):
        return 'id: ' + self.event_id.__repr__() + ' >> name: ' + self.event_name + ' date: ' + str(self.event_date)
