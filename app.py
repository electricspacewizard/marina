from flask import Flask, redirect
from flask import render_template
# from models import db
import psycopg2
import sys
import pprint
from flask import request
import pdb


app = Flask(__name__)
app.debug = True

POSTGRES = {
    'user': 'marina',
    'pw': '',
    'db': 'marina',
    'host': 'localhost',
    'port': '5432'
}


#BUGS - wont let you input loa as a int

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# db.init_app(app)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.args.get('search'):
        searched_boat = request.args.get('search')
        return redirect('/boat/' + searched_boat)
    else:
      return render_template('home.html')

@app.route("/boat/<name>")
def boat(name):
    boat_data = do_search(name)
    return render_template('boat.html', boat=boat_data)


def do_search(searched_ship):
    conn_string = "host='localhost' dbname='marina' user='marina' password='password'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT row_to_json(boats) FROM boats WHERE bname = '" + searched_ship + "'")
    return cursor.fetchall()[0][0]


def addboatdatabase(bname, btype, loa):
    try:
        conn_string = "host='localhost' dbname='marina' user='atz' password='password'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO boats(bname, btype, loa) VALUES('" + bname + "', '" + btype + "', '" + loa + "')")
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


@app.route('/addboat', methods=["POST", "GET"])
def addboat():
    if request.method == "GET":
        return render_template('addboat.html')
    if request.method == "POST":
        bname = request.form['bname']
        btype = request.form['btype']
        loa = request.form['loa']
        successful = addboatdatabase(bname, btype, loa)
        if successful:
            return render_template('addboat.html', data="Boat Succesfully Added")
        else:
            return render_template('addboat.html', data="Boat was not added, check inputs ")



@app.route("/test")
def test():
    return render_template('test.html')


if __name__ == "__main__":
    app.run()
