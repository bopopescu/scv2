from sqlalchemy import *

engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost')

existing_databases = engine.execute("SHOW DATABASES;")

# Results are a list of single item tuples, so unpack each tuple
existing_databases = [d[0] for d in existing_databases]
# Let's display them.
print("The existing databases are:\n",existing_databases)

database = "scv2db"

# Create database if not exists
if database not in existing_databases:
    engine.execute("CREATE DATABASE {0}".format(database))
    print("Created database {0}".format(database))


scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')

metadata = MetaData(scv2_engine)

#if not engine.dialect.has_table(scv2_engine, "user"):
user = Table('user', metadata,
	Column('user_id', Integer,primary_key=True, autoincrement=True),
    Column('firstname', String(16), nullable=False),
    Column('lastname', String(20)),
    Column('username', String(20), nullable=False),
    Column('birthdate', Date),
    Column('mail', String(30),  nullable=False),
    Column('password', String(20), nullable=False),
    Column('picture_link', String(20), nullable=False),
    Column('bio_link', String(20), nullable=False),

)

#if not engine.dialect.has_table(scv2_engine, "item"):
item = Table('item', metadata,
	Column('item_id', Integer,primary_key=True, autoincrement=True),
    Column('title', String(20), nullable=False),
    Column('release_date', Date, nullable=False),
    Column('type_id',Integer, ForeignKey("item_type.item_type_id"), nullable=False),
    Column('image_link', String(60), primary_key=True, nullable=False),
    Column('video_link', String(20), nullable=False),
    Column('desc_link', String(20), nullable=False),
    Column('mean', Float)
)

#if not engine.dialect.has_table(scv2_engine, "item_type"):
item_type = Table('item_type', metadata,
	Column('item_type_id', Integer,primary_key=True, autoincrement=True),
    Column('type_name', String(20), nullable=False)
)

#if not engine.dialect.has_table(scv2_engine, "notation"):
notation = Table('notation', metadata,
    Column('note_id', Integer, primary_key=True, autoincrement=True),
    Column('item_id', Integer, ForeignKey("item.item_id"), nullable=False),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('note', Float),
    Column('review_link', String(20)),
    Column('review_date', DateTime(timezone=True), default=func.now()),
    Column('upvotes',Integer)

)

vote = Table('vote', metadata,
    Column('vote_id',Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('note_id', Integer, ForeignKey("notation.note_id"), nullable=False),
    Column('good', Boolean )
    )

interest = Table('interest', metadata,
    Column('interest_id', Integer,primary_key=True, autoincrement=True),
    Column('tag_id', Integer, ForeignKey("tag.tag_id"), nullable=False),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('item_id', Integer, ForeignKey("item.item_id"), nullable=False),
    Column('interested',Boolean)

)

tag = Table('tag', metadata,
    Column('tag_id', Integer,primary_key=True, autoincrement=True),
    Column('item_id', Integer, ForeignKey("item.item_id"), nullable=False),
    Column('tagname', String(20), nullable=False)
    )

participation = Table('participation', metadata,
    Column('participant_id', Integer,primary_key=True, autoincrement=True),
    Column('item_id', Integer, ForeignKey("item.item_id"), nullable=False),
    Column('participation_nb', Integer, nullable=False)
    )

participant = Table('participant', metadata,
    Column('participant_id', Integer, ForeignKey("participation.participant_id")),
    Column('firstname', String(16), nullable=False),
    Column('lastname', String(20)),
    Column('birthdate', Date),
    Column('picture_link', String(20), nullable=False),
    Column('bio_link', String(20), nullable=False),

)

distinction = Table('distinction', metadata,
    Column('participant_id', Integer, ForeignKey("participation.participant_id")),
    Column('event_id', Integer, ForeignKey("event.event_id")),
    Column('reward',String(30),nullable=False)
    )

event = Table('event', metadata,
    Column('event_id', Integer, primary_key=True, autoincrement=True),
    Column('event_date', Date, nullable=False),
    Column('event_name',String(20), nullable=False)
    )

metadata.create_all()


for table in metadata.sorted_tables:
    print("\n===================================")
    print("Champs de la table: ",table)
    print("===================================\n")
    for column in table.c:
        print(column)



