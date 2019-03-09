from flask import Flask, redirect, send_from_directory
from flask import render_template
from psycopg2.extras import RealDictCursor
# from models import db
import psycopg2
import sys
import pprint
from flask import request
import pdb
import os

app = Flask(__name__)

DB = {
    'user': 'marina',
    'pw': 'password',
    'db': 'marina',
    'host': 'localhost',
    'port': '5432'
}

db_host = 'postgres-db' if os.environ.get('IN_DOCKER') == '1' else 'localhost'
conn_string = f"host='{db_host}' dbname='{DB['db']}' user='{DB['user']}' password='{DB['pw']}'"
db_conn = psycopg2.connect(conn_string)
cursor = db_conn.cursor()


@app.route("/", methods=["POST", "GET"])
def home():
    if request.args.get('search'):
        searched_boat = request.args.get('search')
        return redirect('/boat/' + searched_boat)
    else:
      cursor = db_conn.cursor(cursor_factory=RealDictCursor)
      cursor.execute("SELECT * FROM boats")
      boats = cursor.fetchall()
      db_conn.commit()
      return render_template('home.html', boats=boats)


@app.route('/images/boats/<path:path>')                     #Read up more in the image paths
def send_image(path):
    return send_from_directory('images/boats', path)


@app.route("/boat/<name>")
def boat(name):
    boat_data = do_search(name.capitalize())
    return render_template('boat.html', boat=boat_data)


def do_search(searched_ship):
    cursor.execute(f"SELECT row_to_json(boats) FROM boats WHERE bname='{searched_ship}'")
    response = cursor.fetchall()[0][0]
    db_conn.commit()
    return response


def add_boat_database(bname, btype, loa):
    try:
        cursor.execute(f'''
          INSERT INTO boats(bname, btype, loa)
          VALUES('{bname}', '{btype}', '{loa}') RETURNING id
        ''')
        inserted_id = cursor.fetchone()[0]
        db_conn.commit()
        return inserted_id
    except Exception as e:
        print(e)
        return False

@app.route('/boat/new', methods=["GET"])
def new_boat():
    return render_template('addboat.html')


@app.route('/boat/<name>/edit', methods=["GET"])
def edit_boat(name):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM boats WHERE bname='{name}'")
    boat = cursor.fetchall()[0]
    db_conn.commit()
    return render_template('edit_boat.html', boat=boat)


@app.route('/boat/<name>/delete', methods=["POST"])
def delete_boat(name):
    cursor.execute(f"DELETE from boats WHERE bname='{name}'")
    db_conn.commit()
    return redirect('/')


@app.route('/boat/<name>', methods=["POST"])
def update_boat(name):
  bname = request.form['bname']
  btype = request.form['btype']
  loa = request.form['loa']
  boat_id = request.form['boat_id']

  # get() returns NoneType rather than break with a usual dict lookup
  image = request.files.get('image')

  cursor.execute(f"UPDATE boats SET btype='{btype}', loa='{loa}', bname='{bname}' WHERE bname='{name}'")
  db_conn.commit()

  if image:
    image.save(os.path.join('images/boats', str(boat_id) + '.jpg'))

  return redirect(f'/boat/{bname}')


@app.route('/boat', methods=['POST'])
def add_boat():
    bname = request.form['bname'].capitalize()
    btype = request.form['btype'].capitalize()
    loa = request.form['loa']
    inserted_id = add_boat_database(bname, btype, loa)
    if inserted_id:
        image = request.files['image']
        image.save(os.path.join('images/boats', str(inserted_id) + '.jpg'))
        return redirect('/boat/' + bname)
    else:
        return render_template('addboat.html', data="Boat was not added, check inputs ")


@app.route("/test")
def test():
    return render_template('test.html')


if __name__ == "__main__":
    app.run(debug=True)
