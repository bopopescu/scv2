
from rqst_func_scv2 import *
from base_model_scv2 import *
from flask import Flask 

## Nice func to create N new rows in the table linked to ormClass
 ## the entry 'dict_tuple' is a tuple (or list!) of dicts that contain the ormClass attributes

def insert_db(session,objList):

	for someObj in objList:
		dbAdd(session,someObj)
	session.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://scv2:scv2@localhost/scv2db'
db.init_app(app)
app.app_context().push()

db.drop_all()
db.create_all()


mes_users = [
			User(first_name='alfredo',
		   last_name='freccino',
		   username='freccifredo',
		   birthdate = date(1978,11,24),
		   email = 'fredoIlPomodoro@italia.it',
		   password = 'unamozzarella'),


			User(first_name='Yoan',
            last_name='boayaso',
            username='boyoan',
            birthdate=date(1999,10,11),
            email='yoyoanso@yahoo.fr',
            password='123'),

			User(first_name='truc',
            last_name='bidule',
            username='machin',
            birthdate=date(3001,10,21),
            email='WOW@WOW.wow',
            password='wowowowowow'),

			User(first_name='firstname1',
            last_name='lastname1',
            username='imNUMBA1',
            birthdate=date(1,1,1),
            email='numba@one.first',
            password='imthafirst'),

            User(first_name='boi',
           	last_name='dat',
           	username='o shit waddup',
           	birthdate= date(1996,12,12),
           	email= 'sumfrog@boi.com',
           	password='frogfrog'
           	)
           	]
mes_types = [
				Itemtype(type_name='Movies'),
				Itemtype(type_name='Music'),
				Itemtype(type_name='Books'),
				Itemtype(type_name='Drinks'),
				Itemtype(type_name='Smartphones'),
				Itemtype(type_name='Furnitures'),
				Itemtype(type_name='Technologies'),
				Itemtype(type_name='Jewels'),
				Itemtype(type_name='Watches'),
				Itemtype(type_name='TV Channels')
				]
mes_items = [
				Item(title='babar',
					 release_date=datetime(1969,12,30),
					 type_id= 1,
					 image_link='/some/data/for/babar/1',
					 video_link='/some/data/for/babar/1',
					 desc_link='/some/data/for/babar/1',
					 mean=3.3),

				Item(title='babar',
					 release_date=datetime(1969,12,30),
					 type_id= 3,
					 image_link='/some/data/for/babar/3',
					 video_link='/some/data/for/babar/3',
					 desc_link='/some/data/for/babar/3',
					 mean=1.3),

				Item(title='Archives du Ciné-Club 1970-1999',
					 release_date=datetime(2003,1,3),
					 type_id= 1,
					 image_link='/some/data/for/cineclub',
					 video_link='/some/data/for/cineclub',
					 desc_link='/some/data/for/cineclub',
					 mean=0.9),

				Item(title='Le Fabuleux Destin d\'Amélie Poulain',
					 release_date=datetime(2001,1,1),
					 type_id= 1,
					 image_link='/some/data/for/apoulain',
					 video_link='/some/data/for/apoulain',
					 desc_link='/some/data/for/apoulain',
					 mean=4.7),

				Item(title='Les Amours imaginaires',
					 release_date=datetime(2010,1,3),
					 type_id= 1,
					 image_link='/some/data/for/xdolan/lai',
					 video_link='/some/data/for/cineclub/lai',
					 desc_link='/some/data/for/cineclub/lai',
					 mean=4.1),

				Item(title='Rock Bottom',
					 release_date=datetime(1974,7,26),
					 type_id= 2,
					 image_link='/some/data/for/rwyatt/rb',
					 video_link='/some/data/for/rwyatt/rb',
					 desc_link='/some/data/for/rwyatt/rb',
					 mean=4.9)

			]
			
mes_notations = [
				Notation(
					item_id=1,
					user_id=1,
					note=4,
					review_link='/scv2/big/data/1',
					upvotes=134),

				Notation( 
					item_id=3,
					user_id=1,
					note=2,
					review_link='/scv2/big/data/3',
					upvotes=1),

				Notation( 
					item_id=6,
					user_id=1,
					note=4,
					review_link='/scv2/big/data/6',
					upvotes=6),

				Notation( 
					item_id=1,
					user_id=2,
					note=3,
					review_link='/scv2/big/data/1',
					upvotes=2),

				Notation( 
					item_id=2,
					user_id=2,
					note=3,
					review_link='/scv2/big/data/2',
					upvotes=2),

				Notation( 
					item_id=3,
					user_id=2,
					note=5,
					review_link='/scv2/big/data/3',
					upvotes=2),

				Notation( 
					item_id=2,
					user_id=3,
					note=3,
					review_link='/scv2/big/data/2',
					upvotes=4),

				Notation( 
					item_id=3,
					user_id=3,
					note=2,
					review_link='/scv2/big/data/3',
					upvotes=12),

				Notation( 
					item_id=4,
					user_id=3,
					note=1,
					review_link='/scv2/big/data/4',
					upvotes=6),

				Notation( 
					item_id=5,
					user_id=3,
					note=3,
					review_link='/scv2/big/data/5',
					upvotes=1),

				Notation( 
					item_id=2,
					user_id=4,
					note=3,
					review_link='/scv2/big/data/2',
					upvotes=4),

				Notation( 
					item_id=4,
					user_id=4,
					note=4,
					review_link='/scv2/big/data/4',
					upvotes=4),

				Notation( 
					item_id=6,
					user_id=4,
					note=5,
					review_link='/scv2/big/data/6',
					upvotes=4),

				Notation( 
					item_id=1,
					user_id=5,
					note=1,
					review_link='/scv2/big/data/1',
					upvotes=5),

				Notation( 
					item_id=6,
					user_id=5,
					note=5,
					review_link='/scv2/big/data/1',
					upvotes=1)
				]

mes_participants = [
				
				Participant(firstname='babar',
							lastname='the Elephant',
							birthdate=datetime(1931,1,1),
							picture_link='/scv2/part/babar',
							bio_link='/scv2/part/babar'),

				Participant(firstname='Cécile',
							lastname='de Brunhoff',
							birthdate=datetime(1903,10,16),
							deathdate=datetime(2003,4,7),
							picture_link='/scv2/part/babar/c',
							bio_link='/scv2/part/babar/c'),

				Participant(firstname='Jean',
							lastname='de Brunhoff',
							birthdate=datetime(1899,9,12),
							deathdate=datetime(1937,10,16),
							picture_link='/scv2/part/babar/j',
							bio_link='/scv2/part/babar/j'),

				Participant(firstname='Laurent',
							lastname='de Brunhoff',
							birthdate=datetime(1925,9,30),
							picture_link='/scv2/part/babar/l',
							bio_link='/scv2/part/babar/l'),

				Participant(firstname='Thomas',
							lastname='Viola',
							birthdate=datetime(1996, 2, 23),
							picture_link='/scv2/part/tviola',
							bio_link='/scv2/part/tviola'),

				Participant(firstname='Jean-Pierre',
							lastname='Jeunet',
							birthdate=datetime(1953,9,3),
							picture_link='/scv2/part/jpjeunet',
							bio_link='/scv2/part/jpjeunet'),

				Participant(firstname='Guillaume',
							lastname='Laurent',
							birthdate=datetime(1961,11,22),
							picture_link='/scv2/part/glaurent',
							bio_link='/scv2/part/glaurent'),

				Participant(firstname='Audrey',
							lastname='Tautou',
							birthdate=datetime(1976,8,9),
							picture_link='/scv2/part/atautou',
							bio_link='/scv2/part/atautou'),

				Participant(firstname='Xavier',
							lastname='Dolan',
							birthdate=datetime(1989,3,20),
							picture_link='/scv2/part/xdolan',
							bio_link='/scv2/part/xdolan'),

				Participant(firstname='Monia',
							lastname='Chokri',
							birthdate=datetime(1983,6,27),
							picture_link='/scv2/part/mchokri',
							bio_link='/scv2/part/mchokri'),

				Participant(firstname='Niels',
							lastname='Schneider',
							birthdate=datetime(1987,6,18),
							picture_link='/scv2/part/nschneider',
							bio_link='/scv2/part/nschneider'),

				Participant(firstname='Robert',
							lastname='Wyatt',
							birthdate=datetime(1945,1,28),
							picture_link='/scv2/part/rwyatt',
							bio_link='/scv2/part/rwyatt'),

				Participant(firstname='Mike',
							lastname='Oldfield',
							birthdate=datetime(1953,5,15),
							picture_link='/scv2/part/moldfield',
							bio_link='/scv2/part/moldfield'),

				Participant(firstname='Nick',
							lastname='Mason',
							birthdate=datetime(1944,1,27),
							picture_link='/scv2/part/nmason',
							bio_link='/scv2/part/nmason')

				]


mes_participations = [
						Participation(item_id=1,
									  	participant_id=1,
									  	role='Personnage Principal'),

						Participation(item_id=1,
										participant_id=2,
										role='Créatrice'),

						Participation(item_id=1,
									participant_id=3,
									role='Illustrateur'),

						Participation(item_id=1,
									participant_id=4,
									role='Illustrateur'),

						Participation(item_id=2,
									participant_id=1,
									role='Personnage Principal'),

						Participation(item_id=2,
									participant_id=2,
									role='Créatrice'),

						Participation(item_id=2,
								participant_id=3,
								role='Illustrateur'),

						Participation(item_id=2,
								participant_id=4,
								role='Illustrateur'),

						Participation(item_id=3,
								participant_id=5,
								role='boss'),

						Participation(item_id=4,
								participant_id=6,
								role='Réalisateur et Scénariste'),

						Participation(item_id=4,
								participant_id=7,
								role='Scénariste'),

						Participation(item_id=4,
								participant_id=8,
								role='Actrice principale'),

						Participation(item_id=5,
								participant_id=9,
								role='Réalisateur,Scénariste et Personnage Principal'),

						Participation(item_id=5,
								participant_id=10,
								role='Personnage Principal'),

						Participation(item_id=6,
								participant_id=12,
								role='Compositeur,Vocaux,Claviers,Percussions'),

						Participation(item_id=6,
								participant_id=13,
								role='Guitariste'),

						Participation(item_id=6,
								participant_id=14,
								role='Producteur')
						]


insert_db(db.session,mes_users)
insert_db(db.session,mes_types)
insert_db(db.session,mes_items)
insert_db(db.session,mes_notations)
insert_db(db.session,mes_participants)
insert_db(db.session,mes_participations)





