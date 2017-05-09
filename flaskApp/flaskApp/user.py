#from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from datetime import datetime,timedelta,date

from sqlalchemy import select,and_,func,Date,cast,exc

"""
def dbAdd(session,an_object):
    try:
        session.add(an_object)
        session.flush()

    except exc.IntegrityError:
        print('Integrity Error, add canceled.\n')
        session.rollback()


app = Flask(__name__)
"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'

db = SQLAlchemy(app)

#if not engine.dialect.has_table(scv2_engine, "user"):

class User(db.Model,UserMixin):
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
    
    def __init__(self,id=None,active=None,comfirmed_at=None, first_name=None,last_name=None,username=None,birthdate=None,email=None, password=None,picture_link=None,bio_link=None):
        self.first_name=first_name
        self.id=id
        self.last_name=last_name
        self.username=username
        self.active=active
        self.birthdate=birthdate
        self.email=email
        self.password=password
        self.picture_link=picture_link
        self.bio_link=bio_link
        self.comfirmed_at=comfirmed_at
    
    def __repr__(self):
        return 'name: '+self.first_name+' '+self.last_name+'| username: '+self.username

"""
db.create_all()

# On peut faire appel au constructeur

yoan = User(first_name='Yoan',
            last_name='boayaso',
            username='boyoan',
            birthdate=date(1999,10,11),
            email='yoyoanso@yahoo.fr',
            password='123'
            )

truc = User(first_name='truc',
            last_name='bidule',
            username='machin',
            birthdate=date(3001,10,21),
            email='WOW@WOW.wow',
            password='wowowowowow'
            )

one1 = User(first_name='firstname1',
            last_name='lastname1',
            username='imNUMBA1',
            birthdate=date(1,1,1),
            email='numba@one.first',
            password='imthafirst'
            )


dbAdd(db.session,one1)
dbAdd(db.session,truc)

db.session.commit()
db.session.commit()
db.session.commit()


print('\n------ Let\'s init the database :) ------\n')

for user in User.query.all():
    print(user) #use of __repr__ method :) 
    
"""