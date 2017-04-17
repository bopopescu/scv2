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
    Column('mail', String(60),  nullable=False),
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
	Column('note_id', Integer,primary_key=True, autoincrement=True),
    Column('item_id', Integer, ForeignKey("item.item_id"), nullable=False),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('note', Float),
    Column('review_link', String(20)),
    Column('review_date', DateTime(timezone=True), default=func.now()),
    Column('upvotes',Integer)

)

metadata.create_all()


for table in metadata.sorted_tables:
	print(table)
	for column in table.c:
		print(column)



# interest = Table('interests',metadata,
# 	Column('interest_id', ForeignKey('user.user_name'), primary_key=True, autoincrement='ignore_fk'),
# 	Column('user_name', String(16), nullable=False, ForeignKey('user.user_name')),

