from datetime import date

# use after create_engine and metadata.create_all()

def init_users(users_table,connection):
	try:
		ins = users_table.insert()

		connection.execute(ins,
								 username='oaioa',
								 lastname='Viola',
								 firstname='Thomas',
								 birthdate=date(1996, 2, 23),
								 mail='thomas.viola@hacker.org',
								 password='iamsuchaboss',
								 picture_link='home/boss/data/pictures/',
								 bio_link='home/boss/data/bios/'
								 )

		connection.execute(ins,
								 username='jadynek',
								 lastname='Nekena Ramanandray',
								 firstname='Jady',
								 birthdate=date(1996, 7, 2),
								 mail='jady.nekram@yahoo.fr',
								 password='jadydaj',
								 picture_link='C:/MesDocs/scv/pictures/',
								 bio_link='C:/MesDocs/scv/bios/'
								 )

		connection.execute(ins,
								 username='poquii',
								 lastname='Quentel',
								 firstname='Paul',
								 birthdate=date(1996, 4, 13),
								 mail='paul.quentel@insa-lyon.fr',
								 password='ppppqqqq1304',
								 picture_link='home/pqtel/bin/pictures/',
								 bio_link='home/pqtel/bin/bios/'
								 )

		connection.execute(ins,
								 username='arnoarnoarnoarno',
								 lastname='Veletanlic',
								 firstname='Arno',
								 birthdate=date(1996, 12,16),
								 mail='av@gmail.com',
								 password='superpasswow123',
								 picture_link='home/arno-vel/INSA/pictures/',
								 bio_link='home/arno-vel/INSA/bios/'
								 )

		connection.execute(ins,
								 username='dat-guy',
								 lastname='some',
								 firstname='dude',
								 birthdate=date(1912, 12,19),
								 mail='duder@basicmail.org',
								 password='dontbehatin',
								 picture_link='/etc/bin/python/',
								 bio_link='/etc/bin/python/'
								 )

		print("SUCCESS: init user table\n")
		return 0

	except:
		print('ERROR: could not init users\n')
		raise

	


def init_item(items_table, connection):
	try:
		ins = items_table.insert()

		connection.execute(ins,
								 title='babar',
								 release_date=date(1969,12,30),
								 type_id= 1,
								 image_link='/some/data/for/babar/1',
								 video_link='/some/data/for/babar/1',
								 desc_link='/some/data/for/babar/1',
								 mean=3.3

								 )

		connection.execute(ins,
								 title='babar',
								 release_date=date(1969,12,30),
								 type_id= 3,
								 image_link='/some/data/for/babar/3',
								 video_link='/some/data/for/babar/3',
								 desc_link='/some/data/for/babar/3',
								 mean=1.3

								 )

		connection.execute(ins,
								 title='Archives du Ciné-Club 1970-1999',
								 release_date=date(2003,1,3),
								 type_id= 1,
								 image_link='/some/data/for/cineclub',
								 video_link='/some/data/for/cineclub',
								 desc_link='/some/data/for/cineclub',
								 mean=0.9

								 )

		connection.execute(ins,
								 title='Le Fabuleux Destin d\'Amélie Poulain',
								 release_date=date(2001,1,1),
								 type_id= 1,
								 image_link='/some/data/for/apoulain',
								 video_link='/some/data/for/apoulain',
								 desc_link='/some/data/for/apoulain',
								 mean=4.7

								 )

		connection.execute(ins,
								 title='Les Amours imaginaires',
								 release_date=date(2010,1,3),
								 type_id= 1,
								 image_link='/some/data/for/xdolan/lai',
								 video_link='/some/data/for/cineclub/lai',
								 desc_link='/some/data/for/cineclub/lai',
								 mean=4.1

								 )

		connection.execute(ins,
								 title='Rock Bottom',
								 release_date=date(1974,7,26),
								 type_id= 2,
								 image_link='/some/data/for/rwyatt/rb',
								 video_link='/some/data/for/rwyatt/rb',
								 desc_link='/some/data/for/rwyatt/rb',
								 mean=4.9

								 )

		print("SUCCESS: init items table\n")
		return 0
	except:
		print("ERROR: could not init items\n")
		raise


def init_item_type(itemtype_table, connection):
	try:
		ins = itemtype_table.insert()

		connection.execute(ins,
								 type_name='Film',

								 )

		connection.execute(ins,
								 type_name='Musique',

								 )

		connection.execute(ins,
								 type_name='Livre',

								 )

		connection.execute(ins,
								 type_name='Boisson',

								 )

		connection.execute(ins,
								 type_name='sometype',

								 )
		return 0
	except:
		print("ERROR: could not init itemtypes\n")
		raise


def init_notation(notation_table, connection):
	try:
		ins = notation_table.insert()

		connection.execute(ins,
								item_id=1,
								user_id=1,
								note=4,
								review_link='/scv2/big/data/1',
								upvotes=134)

		connection.execute(ins,
								item_id=3,
								user_id=1,
								note=2,
								review_link='/scv2/big/data/3',
								upvotes=1)

		connection.execute(ins,
								item_id=6,
								user_id=1,
								note=4,
								review_link='/scv2/big/data/6',
								upvotes=6)

		connection.execute(ins,
								item_id=1,
								user_id=2,
								note=3,
								review_link='/scv2/big/data/1',
								upvotes=2)

		connection.execute(ins,
								item_id=2,
								user_id=2,
								note=3,
								review_link='/scv2/big/data/2',
								upvotes=2)

		connection.execute(ins,
								item_id=3,
								user_id=2,
								note=5,
								review_link='/scv2/big/data/3',
								upvotes=2)

		connection.execute(ins,
								item_id=2,
								user_id=3,
								note=3,
								review_link='/scv2/big/data/2',
								upvotes=4)

		connection.execute(ins,
								item_id=3,
								user_id=3,
								note=2,
								review_link='/scv2/big/data/3',
								upvotes=12)

		connection.execute(ins,
								item_id=4,
								user_id=3,
								note=1,
								review_link='/scv2/big/data/4',
								upvotes=6)

		connection.execute(ins,
								item_id=5,
								user_id=3,
								note=3,
								review_link='/scv2/big/data/5',
								upvotes=1)

		connection.execute(ins,
								item_id=2,
								user_id=4,
								note=3,
								review_link='/scv2/big/data/2',
								upvotes=4)

		connection.execute(ins,
								item_id=4,
								user_id=4,
								note=4,
								review_link='/scv2/big/data/4',
								upvotes=4)

		connection.execute(ins,
								item_id=6,
								user_id=4,
								note=5,
								review_link='/scv2/big/data/6',
								upvotes=4)

		connection.execute(ins,
								item_id=1,
								user_id=5,
								note=1,
								review_link='/scv2/big/data/1',
								upvotes=5)

		connection.execute(ins,
								item_id=6,
								user_id=5,
								note=5,
								review_link='/scv2/big/data/1',
								upvotes=1)


		print("SUCCESS: init item_types table\n")
		return 0

	except:
		print("ERROR: could not init item_types \n")
		raise

		
def init_participant(participant_table, connection):
	try:
		ins = participant_table.insert()

		connection.execute(ins,
								firstname='babar',
								lastname='the Elephant',
								birthdate=date(1931,1,1),
								picture_link='/scv2/part/babar',
								bio_link='/scv2/part/babar')

		connection.execute(ins,
								firstname='Cécile',
								lastname='de Brunhoff',
								birthdate=date(1903,10,16),
								deathdate=date(2003,4,7),
								picture_link='/scv2/part/babar/c',
								bio_link='/scv2/part/babar/c')


		connection.execute(ins,
								firstname='Jean',
								lastname='de Brunhoff',
								birthdate=date(1899,9,12),
								deathdate=date(1937,10,16),
								picture_link='/scv2/part/babar/j',
								bio_link='/scv2/part/babar/j')


		connection.execute(ins,
								firstname='Laurent',
								lastname='de Brunhoff',
								birthdate=date(1925,9,30),
								picture_link='/scv2/part/babar/l',
								bio_link='/scv2/part/babar/l')


		connection.execute(ins,
								firstname='Thomas',
								lastname='Viola',
								birthdate=date(1996, 2, 23),
								picture_link='/scv2/part/tviola',
								bio_link='/scv2/part/tviola')


		connection.execute(ins,
								firstname='Jean-Pierre',
								lastname='Jeunet',
								birthdate=date(1953,9,3),
								picture_link='/scv2/part/jpjeunet',
								bio_link='/scv2/part/jpjeunet')

		connection.execute(ins,
								firstname='Guillaume',
								lastname='Laurent',
								birthdate=date(1961,11,22),
								picture_link='/scv2/part/glaurent',
								bio_link='/scv2/part/glaurent')

		connection.execute(ins,
								firstname='Audrey',
								lastname='Tautou',
								birthdate=date(1976,8,9),
								picture_link='/scv2/part/atautou',
								bio_link='/scv2/part/atautou')


		connection.execute(ins,
								firstname='Xavier',
								lastname='Dolan',
								birthdate=date(1989,3,20),
								picture_link='/scv2/part/xdolan',
								bio_link='/scv2/part/xdolan')


		connection.execute(ins,
								firstname='Monia',
								lastname='Chokri',
								birthdate=date(1983,6,27),
								picture_link='/scv2/part/mchokri',
								bio_link='/scv2/part/mchokri')


		connection.execute(ins,
								firstname='Niels',
								lastname='Schneider',
								birthdate=date(1987,6,18),
								picture_link='/scv2/part/nschneider',
								bio_link='/scv2/part/nschneider')


		connection.execute(ins,
								firstname='Robert',
								lastname='Wyatt',
								birthdate=date(1945,1,28),
								picture_link='/scv2/part/rwyatt',
								bio_link='/scv2/part/rwyatt')


		connection.execute(ins,
								firstname='Mike',
								lastname='Oldfield',
								birthdate=date(1953,5,15),
								picture_link='/scv2/part/moldfield',
								bio_link='/scv2/part/moldfield')


		connection.execute(ins,
								firstname='Nick',
								lastname='Mason',
								birthdate=date(1944,1,27),
								picture_link='/scv2/part/nmason',
								bio_link='/scv2/part/nmason')


		print("SUCCESS: init participant table\n")
		return 0

	except:
		print("ERROR: could not init participant \n")
		raise

def init_participation(participation_table, connection):
	try:
		ins = participation_table.insert()

		connection.execute(ins,
								item_id=1,
								participant_id=1,
								role='Personnage Principal')


		connection.execute(ins,
								item_id=1,
								participant_id=2,
								role='Créatrice')


		connection.execute(ins,
								item_id=1,
								participant_id=3,
								role='Illustrateur')


		connection.execute(ins,
								item_id=1,
								participant_id=4,
								role='Illustrateur')

		connection.execute(ins,
								item_id=2,
								participant_id=1,
								role='Personnage Principal')


		connection.execute(ins,
								item_id=2,
								participant_id=2,
								role='Créatrice')


		connection.execute(ins,
								item_id=2,
								participant_id=3,
								role='Illustrateur')


		connection.execute(ins,
								item_id=2,
								participant_id=4,
								role='Illustrateur')



		connection.execute(ins,
								item_id=3,
								participant_id=5,
								role='boss')


		connection.execute(ins,
								item_id=4,
								participant_id=6,
								role='Réalisateur et Scénariste')


		connection.execute(ins,
								item_id=4,
								participant_id=7,
								role='Scénariste')


		connection.execute(ins,
								item_id=4,
								participant_id=8,
								role='Actrice principale')


		connection.execute(ins,
								item_id=5,
								participant_id=9,
								role='Réalisateur,Scénariste et Personnage Principal')


		connection.execute(ins,
								item_id=5,
								participant_id=10,
								role='Personnage Principal'
								)


		connection.execute(ins,
								item_id=5,
								participant_id=11,
								role='Personnage Principal'
								)


		connection.execute(ins,
								item_id=6,
								participant_id=12,
								role='Compositeur,Vocaux,Claviers,Percussions'
								)


		connection.execute(ins,
								item_id=6,
								participant_id=13,
								role='Guitariste'
								)


		connection.execute(ins,
								item_id=6,
								participant_id=13,
								role='Producteur'
								)

		print("SUCCESS: init participation table\n")

	except:
		print("ERROR: could not init participation\n")
		raise



