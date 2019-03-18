from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sports(Base):
    __tablename__ = 'sports'
    id = Column('id', Integer, autoincrement = True, primary_key = True)
    name = Column('name', String(20, convert_unicode = True))

class Items(Base):
    __tablename__ = 'items'
    id = Column('id', Integer, autoincrement = True, primary_key = True)
    cat_id = Column('cat_id', Integer, primary_key = False)
    title = Column('title', String(20, convert_unicode = True))
    description = Column('description', String(3000, convert_unicode = True))

