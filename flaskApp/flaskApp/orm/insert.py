
from scv2_rqstfunc import *
from scv2_base_model import *
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


mes_types = [
				Itemtype(type_name='Film'),
				Itemtype(type_name='Musique'),
				Itemtype(type_name='Livre'),
				Itemtype(type_name='Boisson'),
				Itemtype(type_name='Sometype'),
				Itemtype(type_name='Mobilier'),
				Itemtype(type_name='Technologie'),
				Itemtype(type_name='Bijoux'),
				Itemtype(type_name='Montre')
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
					upvotes=1),
				]

insert_db(db.session,mes_types)
insert_db(db.session,mes_items)
insert_db(db.session,mes_notations)




