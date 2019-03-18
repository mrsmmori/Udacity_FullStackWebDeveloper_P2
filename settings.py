from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

#DATABASE = 'sqlite:///sports'
DATABASE = 'postgresql:///sports'
ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True
)

session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property()
