from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
Engine = create_engine('postgresql:///sports')


class Sports(Base):
    __tablename__ = 'sports'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, primary_key=False)
    title = Column(String(10))
    description = Column(String(250))

#engine = create_engine('postgresql:///sports')
Base.metadata.create_all(Engine)
