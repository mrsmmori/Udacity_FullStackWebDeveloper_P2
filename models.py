#!/usr/bin/env python
import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

sys.dont_write_bytecode = True
Base = declarative_base()


class Sports(Base):
    __tablename__ = 'sports'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(20, convert_unicode=True))
    items = relationship("Items")


class Items(Base):
    __tablename__ = 'items'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    cat_id = Column(Integer, ForeignKey('sports.id', onupdate='CASCADE',
                    ondelete='CASCADE'))
    title = Column('title', String(20, convert_unicode=True))
    description = Column('description', String(3000, convert_unicode=True))
