from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime,timedelta,date

from sqlalchemy import select,and_,func,Date,cast,exc


def dbAdd(session,an_object):
    try:
        session.add(an_object)
        session.flush()

    except exc.IntegrityError:
        print('Integrity Error, add canceled.\n')
        session.rollback()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'

db = SQLAlchemy(app)

#if not engine.dialect.has_table(scv2_engine, "user"):

class User(db.Model):
    user_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(16), nullable=False)
    lastname = db.Column(db.String(20))
    username = db.Column(db.String(20), nullable=False, unique=True)
    birthdate = db.Column(db.DateTime)
    mail = db.Column( db.String(30),  nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False, unique=True)
    picture_link = db.Column(db.String(100))
    bio_link = db.Column(db.String(100))
    active = db.Column('is_active',db.Boolean(), nullable=False, server_default='0')
    comfirmed_at = db.Column(db.DateTime())

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



# On peut faire appel au constructeur

yoan = User(firstname='Yoan',
            lastname='boayaso',
            username='boyoan',
            birthdate=date(1999,10,11),
            mail='yoyoanso@yahoo.fr',
            password='123'
            )

truc = User(firstname='truc',
            lastname='bidule',
            username='machin',
            birthdate=date(3001,10,21),
            mail='WOW@WOW.wow',
            password='wowowowowow'
            )

one1 = User(firstname='firstname1',
            lastname='lastname1',
            username='imNUMBA1',
            birthdate=date(1,1,1),
            mail='numba@one.first',
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