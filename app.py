from flask import Flask, redirect, send_from_directory, render_template, session, flash
from psycopg2.extras import RealDictCursor
from functools import wraps
# from models import db
import psycopg2
from flask import request
import os
import boto3, botocore

# for reading environment variables from .env
#from dotenv import load_dotenv
#load_dotenv()

app = Flask(__name__)

# How does the session use this?
app.config['SECRET_KEY'] = os.urandom(34)

DB = {
    'user': 'marina',
    'pw': 'password',
    'db': 'marina',
    'host': 'localhost',
    'port': '5432'
}

S3_BUCKET = os.getenv('S3_BUCKET')
S3_LOCATION = 'http://{}.s3.amazonaws.com/marina-boat-images/'.format(S3_BUCKET)

db_host = 'postgres-db' if os.environ.get('IN_DOCKER') == '1' else 'localhost'
conn_string = f"host='{db_host}' dbname='{DB['db']}' user='{DB['user']}' password='{DB['pw']}'"
db_conn = psycopg2.connect(conn_string)
cursor = db_conn.cursor()


s3 = boto3.client(
  's3',
  aws_access_key_id=os.getenv('S3_KEY'),
  aws_secret_access_key=os.getenv('S3_SECRET')
)

@app.context_processor
def inject_boat_names():
  cursor = db_conn.cursor(cursor_factory=RealDictCursor)
  cursor.execute("SELECT bname FROM boats")
  boats = cursor.fetchall()
  names = [boat['bname'] for boat in boats]
  db_conn.commit()
  return dict(boat_names=names)

def upload_file_to_s3(file, file_name):
  try:
    s3.upload_fileobj(
      file,
      S3_BUCKET,
      file_name.lower() + '.jpg',
      ExtraArgs={
        "ACL": "public-read",
        "ContentType": file.content_type
      }
    )
  except Exception as e:
    print("Something Happened: ", e)
    return e

  return "{}{}".format(S3_LOCATION, file.filename)


def get_boats():
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM boats")
    boats = cursor.fetchall()
    db_conn.commit()
    return boats

def get_lifts():
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM lifts")
    lifts = cursor.fetchall()
    db_conn.commit()
    return lifts

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect('/')
    return render_template('login.html', error=error)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You are not logged in')
            return redirect('/login')
    return wrap


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')


@app.route("/", methods=["POST", "GET"])
def home():
    if request.args.get('search'):
        searched_boat = request.args.get('search')
        return redirect('/boat/' + searched_boat)
    else:
      boats = get_boats()
      lifts = get_lifts()
      return render_template('home.html', boats=boats, lifts=lifts)


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
@login_required
def new_boat():
    return render_template('addboat.html')


@app.route('/boat/<name>/edit', methods=["GET"])
@login_required
def edit_boat(name):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f"SELECT * FROM boats WHERE bname='{name}'")
    boat = cursor.fetchall()[0]
    db_conn.commit()
    return render_template('edit_boat.html', boat=boat)


@app.route('/boat/<name>/delete', methods=["POST"])
@login_required
def delete_boat(name):
    cursor.execute(f"DELETE from boats WHERE bname='{name}'")
    db_conn.commit()
    return redirect('/')


@app.route('/boat/<name>', methods=["POST"])
@login_required
def update_boat(name):

  bname = request.form['bname']
  btype = request.form['btype']
  loa = request.form['loa']
  boat_id = request.form['boat_id']
  beam = request.form['beam']
  draft = request.form['draft']
  keel_type = request.form['keel_type']
  dead_weight = request.form['dead_weight']
  shaft_type = request.form['shaft_type']

  # get() returns NoneType rather than break with a usual dict lookup
  image = request.files.get('image')

  cursor.execute(f"UPDATE boats SET btype='{btype}', loa='{loa}', bname='{bname}', beam={beam}, draft={draft} WHERE bname='{name}'")
  db_conn.commit()

  if image:
    image.save(os.path.join('images/boats', str(boat_id) + '.jpg'))

  return redirect(f'/boat/{bname}')


@app.route('/boat', methods=['POST'])
@login_required
def add_boat():
    bname = request.form['bname'].capitalize()
    btype = request.form['btype'].capitalize()
    loa = request.form['loa']
    inserted_id = add_boat_database(bname, btype, loa)
    if inserted_id:

        image = request.files['image']
        # image.save(os.path.join('images/boats', str(inserted_id) + '.jpg'))
        upload_file_to_s3(image, bname)
        return redirect('/boat/' + bname)
    else:
        return render_template('addboat.html', data="Boat was not added, check inputs ")


@app.route("/test")
def test():
    return render_template('test.html')


if __name__ == "__main__":
    flask_port = 80 if os.getenv('IN_DOCKER') else 5000
    app.run(debug=True, host='127.0.0.1', port=flask_port)    # changed this from 0.0.0.0, query James