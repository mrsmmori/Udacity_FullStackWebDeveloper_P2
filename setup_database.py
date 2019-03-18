from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext
from models import Base, Sports, Items

app =  Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///sports' 
db = SQLAlchemy(app)

@click.command('init-db')
@with_appcontext
def init_db_command():
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
#    db.session.add(User('Bob Jones', 'bob@gmail.com'))
#    db.session.add(User('Joe Quimby', 'eat@joes.com'))
#    db.session.commit()(init_db_command)

