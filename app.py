#!/usr/bin/env python
from flask import *
from flask_sqlalchemy import SQLAlchemy
import sys
import config
import click
from collections import OrderedDict
from oauth2client.contrib.flask_util import UserOAuth2
from models import Base, Sports, Items


app = Flask(__name__)
app.config.from_object("config.Development")
app.secret_key = "secret_key_is_secret"
db = SQLAlchemy(app)
oauth2 = UserOAuth2(app)


def init_db():
    # Setup database layout
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    sample_sports = [
        'Soccer',
        'Basketball',
        'Baseball',
        'Frisbee',
        'Snowboarding'
        ]
    for name in sample_sports:
        sports = Sports()
        sports.name = name
        db.session.add(sports)
        db.session.commit()

    # Input sample data
    sample_items = [
        ['1', 'The shoes', 'Good condition, Reasonalbe price, good quality'],
        ['1', 'The shirt', 'Not good condition, Price is okay'],
        ['3', 'The bat', 'condition is so-so, but very expensive'],
        ['5', 'Snowboard', 'Good condition, good quality'],
        ['5', 'Snowboard', 'Bad condition, good quality']
    ]
    for cat_id, title, description in sample_items:
        items = Items()
        items.cat_id = cat_id
        items.title = title
        items.description = description
        db.session.add(items)
        db.session.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    click.echo('Initialized the database.')


# root
@app.route('/', methods=['GET'])
def base():
    categories = [i for i in db.session.query(Sports.name)]
    items = [i for i in db.session.query(Items.id, Sports.name, Items.title,
             Items.description).filter(Sports.id == Items.cat_id)
             .order_by(Items.id)]
    items = [(str(i[0]), i[1], i[2], i[3]) for i in items]
    if not oauth2.has_credentials():
        return render_template('index.html', categories=categories,
                               items=items)
    else:
        return render_template('index_login.html', categories=categories,
                               items=items)


# show items
@app.route('/catalog/<category>/items', methods=['GET'])
def show_items(category):
    categories = [i for i in db.session.query(Sports.name)]
    items = [i for i in db.session.query(Items.id, Sports.name, Items.title,
             Items.description).filter(Sports.id == Items.cat_id)
             .filter(Sports.name == category).order_by(Items.id)]
    items = [(str(i[0]), i[1], i[2], i[3]) for i in items]
    if not oauth2.has_credentials():
        return render_template('index.html', categories=categories,
                               items=items)
    else:
        return render_template('index_login.html', categories=categories,
                               items=items)


# show description
@app.route('/catalog/<category>/<item>', methods=['GET'])
def show_description(category, item):
    id, item = item.split("-")
    item = item.replace("_", " ")

    categories = [i for i in db.session.query(Sports.name)]

    items = db.session.query(
        Items.id, Sports.name,
        Items.title,
        Items.description)\
        .filter(Sports.id == Items.cat_id)\
        .filter(Sports.name == category)
    description = db.session.query(Items.description)\
        .filter(Sports.id == Items.cat_id).filter(Items.id == id).first()[0]

    if not oauth2.has_credentials():
        return render_template('index.html', categories=categories,
                               items=items, description=description)
    else:
        return render_template('index_login.html',
                               categories=categories,
                               items=items, category=category, item=item,
                               description=description, id=id)


# login
@app.route('/login', methods=['GET', 'POST'])
@oauth2.required
def login():
    return redirect(url_for('base'))


# logout
@app.route("/logout", methods=['POST'])
@oauth2.required
def logout():
    session.clear()
    return redirect(url_for('base'))


# add_item
@app.route('/add_item', methods=['GET'])
@oauth2.required
def add_item():
    categories = [i for i in db.session.query(Sports.name)]
    return render_template('add_item.html', categories=categories)


# add_item_post
@app.route('/add_item_post', methods=['POST'])
@oauth2.required
def add_item_post():
    name = request.form['category']
    title = request.form['title']
    description = request.form['description']
    cat_id = db.session.query(Sports.id).filter(Sports.name == name).first()
    items = Items()
    items.cat_id = cat_id
    items.title = title
    items.description = description
    db.session.add(items)
    db.session.commit()
    return redirect(url_for('base'))


# edit_item
@app.route('/catalog/<item>/edit', methods=['POST'])
@oauth2.required
def edit_item(item):
    category = request.form['category']
    categories = request.form['categories']
    item = request.form['item']
    description = request.form['description']
    id = request.form['id']
    categories = [i for i in db.session.query(Sports.name)]
    return render_template('edit_item.html', item=item,
                           description=description, category=category,
                           categories=categories, id=id)


# edit_item_post
@app.route('/edit_item_post', methods=['POST'])
@oauth2.required
def edit_item_post():
    id = request.form['id']
    name = request.form['category']
    title = request.form['title']
    description = request.form['description']
    cat_id = db.session.query(Sports.id).filter(Sports.name == name).first()[0]
    id = db.session.query(Items).filter(Items.id == id).first()
    id.cat_id = cat_id
    id.title = title
    id.description = description
    db.session.commit()
    return redirect(url_for('base'))


# delete_item
@app.route('/catalog/<item>/delete', methods=['POST'])
@oauth2.required
def delete_item(item):
    id = request.form['id']
    return render_template('delete_item.html', id=id)


# delete_item_post
@app.route('/delete_item_post', methods=['POST'])
@oauth2.required
def delete_item_post():
    id = request.form['id']
    db.session.query(Items).filter(Items.id == id).delete()
    db.session.commit()
    return redirect(url_for('base'))


# json endpoint
@app.route('/catalog.json')
def catalog_json():
    dict = OrderedDict()
    dict2 = OrderedDict()
    li = []
    entries = [i for i in db.session.query(Sports.id, Sports.name, Items.id,
               Items.cat_id, Items.title, Items.description)
               .filter(Sports.id == Items.cat_id)]
    for entry in entries:
        print entry
        dict['id'] = entry[0]
        dict['name'] = entry[1]
        dict2['id'] = entry[2]
        dict2['cat_id'] = entry[3]
        dict2['title'] = entry[4]
        dict2['description'] = entry[5]
        dict['Item'] = [dict2]
        li.append(dict)
        dict = OrderedDict()
        dict2 = OrderedDict()
    return jsonify({'category': li})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

