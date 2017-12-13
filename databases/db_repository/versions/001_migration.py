from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=20), nullable=False),
    Column('_password', String(length=128)),
    Column('email', String(length=120), nullable=False),
    Column('firstname', String(length=10), nullable=False),
    Column('lastname', String(length=10), nullable=False),
    Column('id_group', Integer),
    Column('age', Integer),
    Column('admin', Boolean),
    Column('registered_on', DateTime),
    Column('last_seen', DateTime),
    Column('email_confirmed', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['_password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['_password'].drop()
