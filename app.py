from flask import Flask, render_template, g, request, redirect, url_for, jsonify, session
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
import sys
import psycopg2.extras
import config
import database
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = 'hogehoge'
app.config.from_object("config.Development")
app.cli.add_command(database.init_db_command)
app.secret_key = "secret key is secret"

auth = HTTPBasicAuth()

users = {
    "abc123": "abc123",     
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


# base
@app.route('/', methods=['GET'])
def base():
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
        cur.execute('select items.id, sports.name, items.title, items.description from items join sports on items.cat_id = sports.id order by items.id asc;')
        items = cur.fetchall()

    if auth.username() == "":    
        return render_template('index.html', categories=categories, items=items)
    else:
        return render_template('index_login.html', categories=categories, items=items)
    

# show items
@app.route('/catalog/<category>/items', methods=['GET'])
def show_items(category):
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
        cur.execute('''select items.id, sports.name, items.title, items.description from items  
                    join sports on items.cat_id = sports.id where sports.name = %s;''', (category,))
        items = cur.fetchall()
    if auth.username() == "":    
        return render_template('index.html', categories=categories, items=items)
    else:
        return render_template('index_login.html', categories=categories, items=items)

# show description
@app.route('/catalog/<category>/<item>', methods=['GET'])
def show_description(category, item):
    id, item = item.split("-")

    print "%%%%%%%%%%%%%%%%%%"
    print id

    item = item.replace("_", " ")
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
        cur.execute('''select items.id, sports.name, items.title, items.description from items  
                    join sports on items.cat_id = sports.id where sports.name = %s;''', (category,))
        items = cur.fetchall()
        cur.execute('''select items.description, items.id from items  
                    join sports on items.cat_id = sports.id where items.id =%s;''', (id,))
        description = cur.fetchone()[0]

    if auth.username() == "":    
        return render_template('index.html', categories=categories, items=items, description=description)
    else:
        return render_template('index_login.html', categories=categories, items=items, \
                category=category, item=item, description=description, id=id)

@app.route('/login', methods=['GET', 'POST'])
@auth.login_required
def login():
    return redirect(url_for('base'))

# logout
@app.route("/logout", methods=['POST'])
@auth.login_required
def logout():
    return ('Logout', 401)

# add_item
@app.route('/add_item', methods=['GET'])
@auth.login_required
def add_item():
    db = database.get_db()
    with db.cursor() as cur:
        cur.execute('select name from sports;')
        categories = cur.fetchall()
    return render_template('add_item.html', categories=categories)

# add_item_post
@app.route('/add_item_post', methods=['POST'])
@auth.login_required
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
        cur.execute('insert into items (cat_id, title, description) values (%s, %s, %s);', (cat_id, title, description))
    db.commit()
    return redirect(url_for('base'))

# edit_item
@app.route('/catalog/<item>/edit', methods=['POST'])
@auth.login_required
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
    return render_template('edit_item.html', item=item, description=description, category=category, categories=categories, id=id)


# edit_item_post
@app.route('/edit_item_post', methods=['POST'])
@auth.login_required
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
        cur.execute('update items set cat_id=%s, title=%s, description=%s where id=%s;', (cat_id, title, description, id))
    db.commit()
    return redirect(url_for('base'))


# delete_item
@app.route('/catalog/<item>/delete', methods=['POST'])
@auth.login_required
def delete_item(item):
    id = request.form['id']
    return render_template('delete_item.html', id=id)

# delete_item_post
@app.route('/delete_item_post', methods=['POST'])
@auth.login_required
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
    with db.cursor() as cur:
        cur.execute('select * from sports;')
        entries = cur.fetchall()
    return jsonify({'category': entries})
        

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=8000)
