from sqlalchemy import create_engine
from database_setup import Base, Sports, Items, Engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=Engine)
session = Session()


#sports = Sports(name='Pizza Palace')
#session.add(sports)
#session.commit()

#read
print([i.name for i in session.query(Sports).all()])
