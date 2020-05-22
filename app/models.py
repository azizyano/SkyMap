from flask import Flask
app = Flask(__name__)

from app import views
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mymusic.db'
app.secret_key = "flask rocks!"

db = SQLAlchemy(app)


class Skylink(db.Model):
    __tablename__ = "skylink"

    id = db.Column(db.Integer, primary_key=True)
    skylink = db.Column(db.String)

    def __init__(self, name):
        """"""
        self.name = name

    def __repr__(self):
        return "<Skylink: {}>".format(self.skylink)


class Location(db.Model):
    """"""
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    

    artist_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    artist = db.relationship("Skylink", backref=db.backref(
        "location", order_by=id), lazy=True)

    def __init__(self, title, release_date, publisher, media_type):
        """"""
        self.location = title
        
