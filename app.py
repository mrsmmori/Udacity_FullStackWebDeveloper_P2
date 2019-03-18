from flask import *
from flask_sqlalchemy import SQLAlchemy
import sys
import psycopg2.extras
import config
# remove
import database

from collections import OrderedDict
from oauth2client.contrib.flask_util import UserOAuth2

from models import Base, Sports, Items


app = Flask(__name__)
app.config.from_object("config.Development")
app.cli.add_command(database.init_db_command)
app.secret_key = "secret_key_is_secret"

oauth2 = UserOAuth2(app)


@app.route('/needs_credentials')
@oauth2.required
def example():
    # http is authorized with the user's credentials and can be used
    # to make http calls.
    http = oauth2.http()

    # Or, you can access the credentials directly
    credentials = oauth2.credentials


# root
@app.route('/', methods=['GET'])
def base():
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
        cur.execute('''select items.id, sports.name, items.title,
                        items.description from items join sports on
                        items.cat_id = sports.id order by items.id asc;''')
        items = cur.fetchall()

    if not oauth2.has_credentials():
        return render_template('index.html', categories=categories,
                               items=items)
    else:
        return render_template('index_login.html', categories=categories,
                               items=items)


# show items
@app.route('/catalog/<category>/items', methods=['GET'])
def show_items(category):
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
        cur.execute('''select items.id, sports.name, items.title,
                    items.description from items join sports on
                    items.cat_id = sports.id where sports.name = %s;''',
                    (category,))
        items = cur.fetchall()
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
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
        cur.execute('''select items.id, sports.name, items.title,
        items.description from items join sports on
        items.cat_id = sports.id where sports.name = %s;''', (category,))
        items = cur.fetchall()
        cur.execute('''select items.description, items.id from items
        join sports on items.cat_id = sports.id
        where items.id =%s;''', (id,))
        description = cur.fetchone()[0]

    if not oauth2.has_credentials():
        return render_template('index.html', categories=categories,
                               items=items, description=description)
    else:
        return render_template('index_login.html', categories=categories,
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
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
    return render_template('add_item.html', categories=categories)


# add_item_post
@app.route('/add_item_post', methods=['POST'])
@oauth2.required
def add_item_post():
    name = request.form['category']
    title = request.form['title']
    description = request.form['description']

    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select id from sports where name = %s;', (name,))
        cat_id = cur.fetchone()
    cat_id = cat_id[0]
    with db.cursor() as cur:
        cur.execute('''insert into items (cat_id, title, description)
                    values (%s, %s, %s);''', (cat_id, title, description))
    db.commit()
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
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
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

    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select id from sports where name = %s;', (name,))
        cat_id = cur.fetchone()
    cat_id = cat_id[0]

    with db.cursor() as cur:
        cur.execute('''update items set cat_id=%s, title=%s,
                        description=%s where id=%s;''',
                    (cat_id, title, description, id))
    db.commit()
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
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('delete from items where id = %s', (id, ))
    db.commit()
    return redirect(url_for('base'))


# json endpoint
@app.route('/catalog.json')
def catalog_json():
    db = database.get_db()
    dict = OrderedDict()
    dict2 = OrderedDict()
    li = []
    with db.cursor() as cur:
        cur.execute('''select sports.id, sports.name, items.id, items.cat_id,
                        items.title, items.description from sports join items
                        on sports.id = items.cat_id;''')
        entries = cur.fetchall()
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

