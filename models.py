from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Boat(db.Model):
    __tablename__ = 'boats'
    id = db.Column(db.Integer, primary_key=True)
    bname = db.Column(db.String(256), unique=True, nullable=False)
    btype = db.Column(db.String(256), unique=True, nullable=False)
    loa = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        pass