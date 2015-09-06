from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
account = Table('account', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('acc_name', String(length=64)),
)

expense = Table('expense', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String(length=140)),
    Column('price', Integer),
    Column('type', String),
    Column('acc_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['account'].create()
    post_meta.tables['expense'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['account'].drop()
    post_meta.tables['expense'].drop()
